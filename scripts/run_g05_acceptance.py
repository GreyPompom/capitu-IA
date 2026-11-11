"""Gera a tabela G05 com evidências separadas de fixtures e Open Library ao vivo."""

from __future__ import annotations

import argparse
import csv
import json
import subprocess
import sys
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Protocol
from uuid import uuid4

import httpx

from app.chat_service import CapituChatService
from app.schemas import BookDetails, BookSummary, ChatRequest, ConversationState, Intent
from services.open_library import OpenLibraryClient, OpenLibraryUnavailableError, RequestPacer


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "evaluation" / "g05_acceptance.csv"
FIELDS = (
    "evidencia_tipo", "id", "entrada", "intencao_esperada", "pre_condicao",
    "modo", "oraculo", "resultado_obtido", "status", "versao", "data", "evidencia",
)


@dataclass(frozen=True)
class Case:
    id: str
    entry: str
    intent: str
    state: tuple[str, ...]
    query: tuple[tuple[str, str], ...]
    oracle: str
    fixture: str = "normal"
    steps: tuple[tuple[str, str | None, int | None], ...] = ()
    live_steps: tuple[tuple[str, str | None, int | None], ...] = ()
    live_state: tuple[str, ...] = ()
    live_query: tuple[tuple[str, str], ...] = ()
    live_min_results: int = 0
    initial: str | None = None


def _case(
    id: str,
    entry: str,
    intent: str,
    state: str,
    query: tuple[tuple[str, str], ...],
    oracle: str,
    *,
    fixture: str = "normal",
    steps: tuple[tuple[str, str | None, int | None], ...] = (),
    live_state: tuple[str, ...] = (),
    live_query: tuple[tuple[str, str], ...] = (),
    live_min_results: int = 0,
    live_steps: tuple[tuple[str, str | None, int | None], ...] = (),
    initial: str | None = None,
) -> Case:
    return Case(
        id, entry, intent, (state,), query, oracle, fixture, steps, live_steps,
        live_state or (state,), live_query or query, live_min_results, initial,
    )


def _step(message: str, state: str | None = None, after: int | None = None) -> tuple[str, str | None, int | None]:
    return message, state, after


ANSWERED = ConversationState.ANSWERED.value
CLARIFY = ConversationState.AWAITING_CLARIFICATION.value
SELECT = ConversationState.AWAITING_SELECTION.value
NO_RESULTS = ConversationState.NO_RESULTS.value
OUT_OF_SCOPE = ConversationState.OUT_OF_SCOPE.value
UNAVAILABLE = ConversationState.SOURCE_UNAVAILABLE.value
TITLE = Intent.SEARCH_TITLE.value
AUTHOR = Intent.SEARCH_AUTHOR_WORKS.value
SUBJECT = Intent.SEARCH_SUBJECT.value
DETAILS = Intent.BOOK_DETAILS.value
SEARCH_STATES = (ANSWERED, SELECT, NO_RESULTS)
T = lambda value: (("title", value),)
A = lambda value: (("author", value),)
S = lambda value: (("subject", value),)
D = lambda key: (("details", key),)

CASES = (
    _case("T01", "Procure Dom Casmurro", TITLE, ANSWERED, T("Dom Casmurro"), "Buscar título e listar candidatos.",
          live_state=SEARCH_STATES),
    _case("T02", "Você encontra o livro A Hora da Estrela?", TITLE, ANSWERED, T("A Hora da Estrela"),
          "Extrair título e listar candidatos.", live_state=SEARCH_STATES),
    _case("T03", "Estou atrás de um livro chamado 1984", TITLE, ANSWERED, T("1984"),
          "Reconhecer a paráfrase e buscar o título.", live_state=SEARCH_STATES),
    _case("T04", "Procure Dom Casmuro", TITLE, ANSWERED, T("Dom Casmuro"),
          "Consultar a grafia dada; fixture retorna Dom Casmurro.", fixture="typo", live_state=SEARCH_STATES),
    _case("T05", "Quais livros Machado de Assis escreveu?", AUTHOR, ANSWERED, A("Machado de Assis"),
          "Buscar obras pelo nome completo do autor.", live_state=SEARCH_STATES),
    _case("T06", "Mostre obras de Clarice Lispector", AUTHOR, ANSWERED, A("Clarice Lispector"),
          "Preservar nome completo do autor.", live_state=SEARCH_STATES),
    _case("T07", "Quero ler algo escrito por George Orwell", AUTHOR, ANSWERED, A("George Orwell"),
          "Reconhecer paráfrase e buscar pelo autor.", live_state=SEARCH_STATES),
    _case("T08", "Quero livros sobre inteligência artificial", SUBJECT, ANSWERED, S("inteligência artificial"),
          "Extrair e buscar o assunto completo.", live_state=SEARCH_STATES),
    _case("T09", "Me mostre ficção científica", SUBJECT, ANSWERED, S("ficção científica"),
          "Extrair o gênero sem incluir o comando.", live_state=SEARCH_STATES),
    _case("T10", "Alguma leitura a respeito de astronomia?", SUBJECT, ANSWERED, S("astronomia"),
          "Reconhecer paráfrase e buscar o assunto.", live_state=SEARCH_STATES),
    _case("T11", "Quem escreveu Dom Casmurro?", DETAILS, ANSWERED,
          T("Dom Casmurro") + D("/works/OL1003134W"),
          "Apresentar autoria e fonte do título.",
          live_state=(ANSWERED, SELECT), live_query=T("Dom Casmurro") + D("*"), live_min_results=1,
          live_steps=(_step("o primeiro", SELECT), _step("quem escreveu?", ANSWERED, after=0))),
    _case("T12", "Quero saber mais sobre A Hora da Estrela", DETAILS, ANSWERED,
          T("A Hora da Estrela") + D("/works/OL1003134W"),
          "Consultar detalhes ou pedir seleção.", live_state=(ANSWERED, SELECT),
          live_query=T("A Hora da Estrela")),
    _case("T13", "Livros de história", "n/a", CLARIFY, (),
          "Pedir esclarecimento sem chamar catálogo; oráculo aprovado em 2026-11-10."),
    _case("T14", "Machado", "n/a", CLARIFY, (), "Pedir esclarecimento sem assumir pessoa ou operação."),
    _case("T15", "Busque um livro", TITLE, CLARIFY, (), "Perguntar o título sem consultar catálogo."),
    _case("T16", "Mostre livros de um autor", AUTHOR, CLARIFY, (),
          "Perguntar o autor; não interpretar a expressão genérica como assunto."),
    _case("T17", "Qual a previsão do tempo?", "n/a", OUT_OF_SCOPE, (),
          "Abster-se sem consultar catálogo."),
    _case("T18", "Renove meu empréstimo", "n/a", OUT_OF_SCOPE, (),
          "Explicar que empréstimos estão fora do escopo."),
    _case("T19", "Procure Zyx Livro 8472", TITLE, NO_RESULTS, T("Zyx Livro 8472"),
          "Fixture vazia informa que não encontrou nesta fonte.", fixture="empty", live_state=SEARCH_STATES),
    _case("T20", "Obras de Zyx Autor 8472", AUTHOR, NO_RESULTS, A("Zyx Autor 8472"),
          "Fixture vazia informa que não encontrou nesta fonte.", fixture="empty", live_state=SEARCH_STATES),
    _case("T21", "Procure 1984", TITLE, UNAVAILABLE, T("1984"),
          "Falha injetada gera indisponibilidade, sem crash.", fixture="timeout"),
    _case("T22", "Procure Dom Casmurro", TITLE, SELECT, T("Dom Casmurro"),
          "Dois resultados levam à seleção.", fixture="multiple",
          live_state=(SELECT,), live_min_results=2),
    _case("T23", "Procure Dom Casmurro → o segundo → quem escreveu?", DETAILS, ANSWERED,
          T("Dom Casmurro") + D("/works/OL103123W"), "Selecionar o segundo item e mostrar sua autoria.",
          fixture="multiple",
          steps=(_step("o segundo", SELECT), _step("quem escreveu?", ANSWERED, after=0)),
          live_query=T("Dom Casmurro") + D("*"), live_min_results=2, initial="Procure Dom Casmurro"),
    _case("T24", "Busca por Orwell → nova busca sobre astronomia", SUBJECT, ANSWERED,
          A("George Orwell") + S("astronomia"), "Nova busca não reutiliza o autor anterior.",
          steps=(_step("Agora quero livros sobre astronomia"),), live_state=SEARCH_STATES,
          initial="Quero ler algo escrito por George Orwell"),
)


class Catalog(Protocol):
    calls: list[tuple[str, str]]

    def search_by_title(self, title: str) -> list[BookSummary]: ...
    def search_by_author(self, author: str) -> list[BookSummary]: ...
    def search_by_subject(self, subject: str) -> list[BookSummary]: ...
    def get_details(self, openlibrary_key: str, *, fallback_authors: tuple[str, ...] = ()) -> BookDetails: ...


class FixtureCatalog:
    def __init__(self, mode: str) -> None:
        self.mode = mode
        self.calls: list[tuple[str, str]] = []
        self.books: dict[str, BookSummary] = {}

    def _book(self, key: str, title: str, authors: list[str]) -> BookSummary:
        book = BookSummary(
            openlibrary_key=key, title=title, authors=authors,
            source_url=f"https://openlibrary.org{key}",
        )
        self.books[key] = book
        return book

    def search_by_title(self, title: str) -> list[BookSummary]:
        self.calls.append(("title", title))
        if self.mode == "timeout":
            raise OpenLibraryUnavailableError("Falha controlada G05.")
        if self.mode == "empty":
            return []
        if self.mode == "multiple":
            return [
                self._book("/works/OL1003134W", "Dom Casmurro", ["Machado de Assis"]),
                self._book("/works/OL103123W", "Segundo", ["Autor 2"]),
            ]
        if self.mode == "typo":
            return [self._book("/works/OL1003134W", "Dom Casmurro", ["Machado de Assis"])]
        return [self._book("/works/OL1003134W", title, ["Machado de Assis"])]

    def search_by_author(self, author: str) -> list[BookSummary]:
        self.calls.append(("author", author))
        return [] if self.mode == "empty" else [
            self._book("/works/OL1003134W", "Dom Casmurro", [author])
        ]

    def search_by_subject(self, subject: str) -> list[BookSummary]:
        self.calls.append(("subject", subject))
        return [self._book("/works/OL103123W", "Fahrenheit 451", ["Ray Bradbury"])]

    def get_details(self, openlibrary_key: str, *, fallback_authors: tuple[str, ...] = ()) -> BookDetails:
        self.calls.append(("details", openlibrary_key))
        book = self.books[openlibrary_key]
        return BookDetails(
            openlibrary_key=openlibrary_key, title=book.title,
            authors=list(fallback_authors) or book.authors,
            source_url=book.source_url, description="Registro controlado G05.",
        )


class RecordingCatalog:
    def __init__(self, client: OpenLibraryClient) -> None:
        self.client = client
        self.calls: list[tuple[str, str]] = []

    def search_by_title(self, value: str) -> list[BookSummary]:
        self.calls.append(("title", value))
        return self.client.search_by_title(value)

    def search_by_author(self, value: str) -> list[BookSummary]:
        self.calls.append(("author", value))
        return self.client.search_by_author(value)

    def search_by_subject(self, value: str) -> list[BookSummary]:
        self.calls.append(("subject", value))
        return self.client.search_by_subject(value)

    def get_details(self, key: str, *, fallback_authors: tuple[str, ...] = ()) -> BookDetails:
        self.calls.append(("details", key))
        return self.client.get_details(key, fallback_authors=fallback_authors)


def _version() -> str:
    result = subprocess.run(
        ["git", "rev-parse", "--short", "HEAD"], cwd=ROOT, check=True,
        capture_output=True, text=True,
    )
    return f"{result.stdout.strip()} + working tree"


def _turns(
    case: Case,
    catalog: Catalog,
    steps: tuple[tuple[str, str | None, int | None], ...],
    events: list[dict[str, object]] | None = None,
) -> list[dict[str, object]]:
    service, session = CapituChatService(catalog=catalog), uuid4()
    turns: list[dict[str, object]] = []
    previous_state: str | None = None
    completed_steps: set[int] = set()

    sequence = ((case.initial or case.entry, None, None), *steps)
    for index, (prompt, required_state, after_step) in enumerate(sequence):
        if required_state and previous_state != required_state:
            continue
        if after_step is not None and after_step not in completed_steps:
            continue
        event_start, call_start = len(events or []), len(catalog.calls)
        response = service.handle(ChatRequest(message=prompt, session_id=session))
        turns.append({
            "input": prompt,
            "state": response.state.value,
            "intent": response.intent.value if response.intent else None,
            "results": [
                {"title": book.title, "authors": book.authors, "source_url": str(book.source_url)}
                for book in response.results
            ],
            "calls": catalog.calls[call_start:],
            "http": events[event_start:] if events is not None else [],
            "text": response.text,
        })
        previous_state = response.state.value
        if index:
            completed_steps.add(index - 1)
    return turns


def _matches(turns: list[dict[str, object]], state: tuple[str, ...], intent: str,
             calls: tuple[tuple[str, str], ...], allow_details: bool = False) -> bool:
    if not turns:
        return False
    final = turns[-1]
    observed_calls = tuple(call for turn in turns for call in turn["calls"])
    expected_intent = None if intent == "n/a" or final["state"] == UNAVAILABLE else intent
    valid_calls = len(observed_calls) == len(calls) and all(
        op == actual_op and (value == "*" or value == actual_value)
        for (op, value), (actual_op, actual_value) in zip(calls, observed_calls)
    )
    if allow_details and len(observed_calls) == len(calls) + 1:
        valid_calls = observed_calls[:-1] == calls and observed_calls[-1][0] == "details"
    return final["state"] in state and final["intent"] == expected_intent and valid_calls


def _row(case: Case, kind: str, mode: str, turns: list[dict[str, object]], status: str,
         evidence: str, version: str, run_date: str) -> dict[str, str]:
    return {
        "evidencia_tipo": kind, "id": case.id, "entrada": case.entry,
        "intencao_esperada": case.intent, "pre_condicao": "Sessão limpa; sessão mantida entre turnos.",
        "modo": mode, "oraculo": case.oracle,
        "resultado_obtido": json.dumps(turns, ensure_ascii=False, separators=(",", ":")),
        "status": status, "versao": version, "data": run_date, "evidencia": evidence,
    }


def _fixture_row(case: Case, version: str, run_date: str) -> dict[str, str]:
    catalog = FixtureCatalog(case.fixture)
    turns = _turns(case, catalog, case.steps)
    status = "passou" if _matches(turns, case.state, case.intent, case.query) else "falhou"
    evidence = "Fixture local; sem rede; scripts/run_g05_acceptance.py"
    if case.fixture == "timeout":
        evidence += (
            "; indisponibilidade controlada; integração E09 em "
            "tests/test_chat_integration.py e retentativas E10 em "
            "tests/test_open_library_resilience.py"
        )
    return _row(case, "fixture", "Catálogo controlado", turns, status,
                evidence, version, run_date)


def _live_row(case: Case, catalog: RecordingCatalog, events: list[dict[str, object]],
              version: str, run_date: str) -> dict[str, str]:
    if case.fixture == "timeout":
        return _row(case, "live", "Não aplicável", [], "pendente",
                    "Indisponibilidade não provocada na API real; evidência controlada está na linha fixture.",
                    version, run_date)
    turns = _turns(case, catalog, case.live_steps or case.steps, events)

    if any(turn["state"] == UNAVAILABLE for turn in turns):
        status = "pendente"
    elif case.live_min_results and len(turns[0]["results"]) < case.live_min_results:
        status = "pendente"
    else:
        status = "passou" if _matches(
            turns, case.live_state, case.intent, case.live_query, allow_details=case.intent == DETAILS
        ) else "falhou"
    return _row(case, "live", LIVE_MODE, turns, status,
                "Open Library ao vivo via E09; respostas HTTP registradas.", version, run_date)


LIVE_MODE = "Open Library ao vivo via E09"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mode", choices=("fixture", "live", "both"), default="both")
    mode = parser.parse_args().mode
    version, run_date = _version(), date.today().isoformat()
    existing = []
    if OUTPUT.exists():
        with OUTPUT.open(encoding="utf-8-sig", newline="") as source:
            existing = [row for row in csv.DictReader(source) if row["evidencia_tipo"] not in _replaced(mode)]
    rows = existing
    failures = 0

    if mode in {"fixture", "both"}:
        for case in CASES:
            row = _fixture_row(case, version, run_date)
            rows.append(row)
            failures += row["status"] == "falhou"
            print(f"fixture {case.id}: {row['status']}")

    if mode in {"live", "both"}:
        events: list[dict[str, object]] = []

        def record(response: httpx.Response) -> None:
            events.append({"status_code": response.status_code, "url": str(response.request.url)})

        http_client = httpx.Client(
            base_url="https://openlibrary.org",
            timeout=httpx.Timeout(8.0),
            headers={"User-Agent": "CAPITU-IA/0.1 (projeto universitario)"},
            event_hooks={"response": [record]},
        )
        pacer = RequestPacer(minimum_interval_seconds=1.0)
        try:
            for case in CASES:
                client = OpenLibraryClient(client=http_client, pacer=pacer)
                row = _live_row(case, RecordingCatalog(client), events, version, run_date)
                rows.append(row)
                failures += row["status"] == "falhou"
                print(f"live {case.id}: {row['status']}")
        finally:
            http_client.close()

    rows.sort(key=lambda row: (row["id"], row["evidencia_tipo"]))
    with OUTPUT.open("w", encoding="utf-8-sig", newline="") as output:
        writer = csv.DictWriter(output, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)
    counts = {(kind, status): sum(r["evidencia_tipo"] == kind and r["status"] == status for r in rows)
              for kind in ("fixture", "live") for status in ("passou", "falhou", "pendente")}
    print(f"Tabela: {OUTPUT.relative_to(ROOT)}; linhas={len(rows)}; status={counts}")
    return int(failures > 0)


def _replaced(mode: str) -> set[str]:
    return {"fixture"} if mode == "fixture" else {"live"} if mode == "live" else {"fixture", "live"}


if __name__ == "__main__":
    sys.exit(main())
