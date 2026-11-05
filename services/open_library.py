"""Cliente HTTP da Open Library, isolado de regras de PLN e diálogo."""

from __future__ import annotations

import re
from typing import Any

import httpx

from app.schemas import BookDetails, BookSummary
from services.normalization import OpenLibraryPayloadError, normalize_detail_payload, normalize_search_document


BASE_URL = "https://openlibrary.org"
SEARCH_PATH = "/search.json"
SEARCH_FIELDS = "key,title,author_name,first_publish_year,edition_count,isbn,subject,cover_i"


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
    ) -> None:
        if not 1 <= limit <= 5:
            raise ValueError("O limite de resultados deve estar entre 1 e 5.")
        self.base_url = base_url.rstrip("/")
        self.limit = limit
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
        try:
            response = self._client.get(path, params=params)
            response.raise_for_status()
            payload = response.json()
        except (httpx.HTTPError, ValueError) as error:
            raise OpenLibraryUnavailableError("Não foi possível consultar a Open Library.") from error
        if not isinstance(payload, dict):
            raise OpenLibraryUnavailableError("A Open Library retornou JSON em formato inesperado.")
        return payload


def _required_query(value: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError("O texto da consulta não pode estar vazio.")
    return " ".join(value.split())


def _safe_detail_key(value: str) -> str:
    if not isinstance(value, str) or not re.fullmatch(r"/(?:works|books)/OL\d+[WM]", value):
        raise ValueError("A chave de detalhe deve ser uma chave de obra ou edição da Open Library.")
    return value
