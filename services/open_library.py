"""Cliente HTTP da Open Library, isolado de regras de PLN e diálogo."""

from __future__ import annotations

import re
from email.utils import parsedate_to_datetime
from datetime import datetime, timezone
import json
from threading import RLock
from time import monotonic, sleep
from typing import Any

import httpx

from app.schemas import BookDetails, BookSummary
from services.normalization import OpenLibraryPayloadError, normalize_detail_payload, normalize_search_document
from services.cache import ResponseCache


BASE_URL = "https://openlibrary.org"
SEARCH_PATH = "/search.json"
SEARCH_FIELDS = "key,title,author_name,first_publish_year,edition_count,isbn,subject,cover_i"
DEFAULT_RETRY_DELAY_SECONDS = 0.25
MAX_RETRY_AFTER_SECONDS = 5.0


class RequestPacer:
    """Reserva espaçamento entre requisições de todas as sessões do processo."""

    def __init__(self, *, minimum_interval_seconds: float, clock=monotonic, sleeper=sleep) -> None:
        if minimum_interval_seconds < 0:
            raise ValueError("O intervalo mínimo não pode ser negativo.")
        self.minimum_interval_seconds = minimum_interval_seconds
        self._clock = clock
        self._sleeper = sleeper
        self._next_allowed = 0.0
        self._lock = RLock()

    def wait(self) -> None:
        with self._lock:
            now = self._clock()
            delay = max(0.0, self._next_allowed - now)
            self._next_allowed = max(now, self._next_allowed) + self.minimum_interval_seconds
        if delay:
            self._sleeper(delay)


class OpenLibraryUnavailableError(RuntimeError):
    """Timeout, erro HTTP ou payload não utilizável da fonte externa."""


class OpenLibraryClient:
    """Consulta a Open Library com limite baixo e transporte substituível em testes."""

    def __init__(
        self,
        client: httpx.Client | None = None,
        *,
        base_url: str = BASE_URL,
        timeout_seconds: float = 8.0,
        limit: int = 5,
        contact_email: str | None = None,
        cache: ResponseCache | None = None,
        pacer: RequestPacer | None = None,
        max_retries: int = 1,
        retry_delay_seconds: float = DEFAULT_RETRY_DELAY_SECONDS,
        sleeper=sleep,
        utcnow=lambda: datetime.now(timezone.utc),
    ) -> None:
        if not 1 <= limit <= 5:
            raise ValueError("O limite de resultados deve estar entre 1 e 5.")
        if max_retries < 0:
            raise ValueError("O número de retentativas não pode ser negativo.")
        self.base_url = base_url.rstrip("/")
        self.limit = limit
        self.max_retries = max_retries
        self.retry_delay_seconds = retry_delay_seconds
        self._sleeper = sleeper
        self._utcnow = utcnow
        self.cache = cache or ResponseCache()
        # Sem contato identificado, segue o limite padrão de 1 requisição/s
        # observado na documentação oficial; com contato configurado, 3 req/s.
        self.pacer = pacer or RequestPacer(minimum_interval_seconds=(1 / 3 if contact_email else 1.0))
        self._owns_client = client is None
        user_agent = "CAPITU-IA/0.1 (projeto universitario)"
        if contact_email:
            user_agent = f"CAPITU-IA/0.1 ({contact_email})"
        self._client = client or httpx.Client(
            base_url=self.base_url,
            timeout=httpx.Timeout(timeout_seconds),
            headers={"User-Agent": user_agent},
        )

    def close(self) -> None:
        if self._owns_client:
            self._client.close()

    def __enter__(self) -> "OpenLibraryClient":
        return self

    def __exit__(self, *_: object) -> None:
        self.close()

    def search_by_title(self, title: str) -> list[BookSummary]:
        return self._search({"title": _required_query(title)})

    def search_by_author(self, author: str) -> list[BookSummary]:
        return self._search({"author": _required_query(author)})

    def search_by_subject(self, subject: str) -> list[BookSummary]:
        # A sondagem G04 confirmou a forma `q=subject:termo` para assuntos.
        return self._search({"q": f"subject:{_required_query(subject)}"})

    def get_details(self, openlibrary_key: str, *, fallback_authors: tuple[str, ...] = ()) -> BookDetails:
        key = _safe_detail_key(openlibrary_key)
        payload = self._get_json(f"{key}.json", params=None)
        try:
            return normalize_detail_payload(payload, fallback_authors=fallback_authors)
        except OpenLibraryPayloadError as error:
            raise OpenLibraryUnavailableError("A Open Library retornou detalhes incompletos ou inválidos.") from error

    def _search(self, query: dict[str, str]) -> list[BookSummary]:
        payload = self._get_json(
            SEARCH_PATH,
            params={**query, "limit": str(self.limit), "fields": SEARCH_FIELDS},
        )
        documents = payload.get("docs")
        if not isinstance(documents, list):
            raise OpenLibraryUnavailableError("A Open Library retornou uma busca sem lista de documentos.")

        books: list[BookSummary] = []
        for document in documents[: self.limit]:
            if not isinstance(document, dict):
                continue
            try:
                books.append(normalize_search_document(document))
            except OpenLibraryPayloadError:
                # Um registro defeituoso não autoriza fabricar dados nem impede
                # que os outros candidatos válidos sejam mostrados.
                continue
        return books

    def _get_json(self, path: str, *, params: dict[str, str] | None) -> dict[str, Any]:
        cache_key = _cache_key(path, params)
        cached = self.cache.get(cache_key)
        if cached is not None:
            return cached

        last_error: Exception | None = None
        for attempt in range(self.max_retries + 1):
            try:
                self.pacer.wait()
                response = self._client.get(path, params=params)
            except (httpx.TimeoutException, httpx.NetworkError) as error:
                last_error = error
                if attempt < self.max_retries:
                    self._sleeper(self.retry_delay_seconds)
                    continue
                break

            if response.status_code in {429} or 500 <= response.status_code <= 599:
                last_error = httpx.HTTPStatusError("Resposta transitória", request=response.request, response=response)
                delay = _retry_delay(response.headers.get("Retry-After"), self._utcnow)
                if attempt < self.max_retries and delay is not None:
                    self._sleeper(delay)
                    continue
                break
            try:
                response.raise_for_status()
                payload = response.json()
            except (httpx.HTTPError, ValueError) as error:
                # JSON inválido e 4xx não transitório não são repetidos.
                last_error = error
                break
            if not isinstance(payload, dict):
                last_error = ValueError("JSON não é objeto")
                break
            self.cache.set(cache_key, payload)
            return payload

        raise OpenLibraryUnavailableError("Não foi possível consultar a Open Library no momento.") from last_error


def _required_query(value: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError("O texto da consulta não pode estar vazio.")
    return " ".join(value.split())


def _safe_detail_key(value: str) -> str:
    if not isinstance(value, str) or not re.fullmatch(r"/(?:works|books)/OL\d+[WM]", value):
        raise ValueError("A chave de detalhe deve ser uma chave de obra ou edição da Open Library.")
    return value


def _cache_key(path: str, params: dict[str, str] | None) -> str:
    return f"{path}?{json.dumps(params or {}, ensure_ascii=False, sort_keys=True, separators=(',', ':'))}"


def _retry_delay(value: str | None, utcnow) -> float | None:
    """Converte Retry-After; prazo excessivo aborta em vez de retentar cedo."""

    if value is None:
        return DEFAULT_RETRY_DELAY_SECONDS
    value = value.strip()
    if value.isdigit():
        delay = float(value)
    else:
        try:
            target = parsedate_to_datetime(value)
            if target.tzinfo is None:
                target = target.replace(tzinfo=timezone.utc)
            delay = max(0.0, (target - utcnow()).total_seconds())
        except (TypeError, ValueError, IndexError):
            return DEFAULT_RETRY_DELAY_SECONDS
    return delay if delay <= MAX_RETRY_AFTER_SECONDS else None
