"""Reproduce the seven initial G05 failures without network access."""

from __future__ import annotations

import argparse
import csv
import json
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from uuid import uuid4

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.chat_service import CapituChatService
from app.schemas import BookDetails, BookSummary, ChatRequest, ConversationState, Intent


@dataclass(frozen=True)
class ReproductionCase:
    identifier: str
    message: str
    expected_intent: Intent | None
    expected_state: ConversationState
    expected_calls: tuple[tuple[str, str], ...]
    expected_behavior: str


CASES = (
    ReproductionCase(
        "T03",
        "Estou atrás de um livro chamado 1984",
        Intent.SEARCH_TITLE,
        ConversationState.ANSWERED,
        (("title", "1984"),),
        "Buscar pelo título 1984.",
    ),
    ReproductionCase(
        "T06",
        "Mostre obras de Clarice Lispector",
        Intent.SEARCH_AUTHOR_WORKS,
        ConversationState.ANSWERED,
        (("author", "Clarice Lispector"),),
        "Buscar obras de Clarice Lispector.",
    ),
    ReproductionCase(
        "T09",
        "Me mostre ficção científica",
        Intent.SEARCH_SUBJECT,
        ConversationState.ANSWERED,
        (("subject", "ficção científica"),),
        "Buscar pelo assunto ficção científica, sem o comando.",
    ),
    ReproductionCase(
        "T10",
        "Alguma leitura a respeito de astronomia?",
        Intent.SEARCH_SUBJECT,
        ConversationState.ANSWERED,
        (("subject", "astronomia"),),
        "Buscar pelo assunto astronomia.",
    ),
    ReproductionCase(
        "T12",
        "Quero saber mais sobre A Hora da Estrela",
        Intent.BOOK_DETAILS,
        ConversationState.ANSWERED,
        (("title", "A Hora da Estrela"), ("details", "/works/OL1W")),
        "Consultar detalhes de A Hora da Estrela.",
    ),
    ReproductionCase(
        "T16",
        "Mostre livros de um autor",
        None,
        ConversationState.AWAITING_CLARIFICATION,
        (),
        "Pedir o nome do autor sem consultar o catálogo.",
    ),
    ReproductionCase(
        "T20",
        "Obras de Zyx Autor 8472",
        Intent.SEARCH_AUTHOR_WORKS,
        ConversationState.NO_RESULTS,
        (("author", "Zyx Autor 8472"),),
        "Buscar o autor; informar lista vazia da fixture.",
    ),
)


class ControlledCatalog:
    """Deterministic catalog fixture that records every requested operation."""

    def __init__(self) -> None:
        self.calls: list[tuple[str, str]] = []

    def search_by_title(self, title: str) -> list[BookSummary]:
        self.calls.append(("title", title))
        return [
            BookSummary(
                openlibrary_key="/works/OL1W",
                title=title,
                authors=["Autor controlado"],
                source_url="https://openlibrary.org/works/OL1W",
            )
        ]

    def search_by_author(self, author: str) -> list[BookSummary]:
        self.calls.append(("author", author))
        if author == "Zyx Autor 8472":
            return []
        return [
            BookSummary(
                openlibrary_key="/works/OL1W",
                title="Obra controlada",
                authors=[author],
                source_url="https://openlibrary.org/works/OL1W",
            )
        ]

    def search_by_subject(self, subject: str) -> list[BookSummary]:
        self.calls.append(("subject", subject))
        return [
            BookSummary(
                openlibrary_key="/works/OL1W",
                title="Obra controlada",
                authors=["Autor controlado"],
                source_url="https://openlibrary.org/works/OL1W",
            )
        ]

    def get_details(
        self, openlibrary_key: str, *, fallback_authors: tuple[str, ...] = ()
    ) -> BookDetails:
        self.calls.append(("details", openlibrary_key))
        return BookDetails(
            openlibrary_key=openlibrary_key,
            title="A Hora da Estrela",
            authors=list(fallback_authors) or ["Autor controlado"],
            source_url=f"https://openlibrary.org{openlibrary_key}",
            description="Detalhes da fixture controlada.",
        )


def _git_version() -> str:
    return subprocess.run(
        ["git", "rev-parse", "--short", "HEAD"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


def _signature(row: dict[str, str]) -> tuple[str, ...]:
    return (
        row["obtido_intencao"],
        row["obtido_estado"],
        row["obtidas_chamadas_catalogo"],
        row["obtido_texto"],
    )


def run(repeats: int, output_path: Path) -> int:
    catalog = ControlledCatalog()
    service = CapituChatService(catalog=catalog)
    version = _git_version()
    records: list[dict[str, str]] = []

    for case in CASES:
        case_records: list[dict[str, str]] = []
        for repetition in range(1, repeats + 1):
            call_start = len(catalog.calls)
            response = service.handle(
                ChatRequest(message=case.message, session_id=uuid4())
            )
            actual_calls = catalog.calls[call_start:]
            expected_intent = case.expected_intent.value if case.expected_intent else ""
            actual_intent = response.intent.value if response.intent else ""
            expected_calls = json.dumps(case.expected_calls, ensure_ascii=False)
            actual_calls_json = json.dumps(actual_calls, ensure_ascii=False)
            passed = (
                actual_intent == expected_intent
                and response.state is case.expected_state
                and actual_calls == list(case.expected_calls)
            )
            record = {
                "id": case.identifier,
                "repeticao": str(repetition),
                "entrada": case.message,
                "modo": "controlado_sem_rede",
                "esperado": case.expected_behavior,
                "esperado_intencao": expected_intent,
                "esperado_estado": case.expected_state.value,
                "esperadas_chamadas_catalogo": expected_calls,
                "obtido_intencao": actual_intent,
                "obtido_estado": response.state.value,
                "obtidas_chamadas_catalogo": actual_calls_json,
                "obtido_texto": response.text,
                "passou": "sim" if passed else "não",
                "versao": version,
                "evidencia": "scripts/run_g06_reproduction.py; fixture determinística; sem rede",
            }
            case_records.append(record)

        signatures = {_signature(record) for record in case_records}
        consistent = len(signatures) == 1
        for record in case_records:
            record["consistente_entre_repeticoes"] = "sim" if consistent else "não"
            records.append(record)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8-sig", newline="") as output_file:
        writer = csv.DictWriter(output_file, fieldnames=list(records[0]))
        writer.writeheader()
        writer.writerows(records)

    failed_cases = sum(
        1
        for case in CASES
        if any(
            row["id"] == case.identifier and row["passou"] == "não"
            for row in records
        )
    )
    inconsistent_cases = sum(
        1
        for case in CASES
        if any(
            row["id"] == case.identifier
            and row["consistente_entre_repeticoes"] == "não"
            for row in records
        )
    )
    print(
        f"{len(CASES) - failed_cases}/{len(CASES)} casos passaram; "
        f"{failed_cases} com divergência do oráculo; "
        f"{inconsistent_cases} inconsistentes em {repeats} repetições."
    )
    print(f"Evidência: {output_path}")
    return 1 if failed_cases or inconsistent_cases else 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--repeats",
        type=int,
        default=3,
        help="Execuções controladas por caso (padrão: 3).",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=ROOT / "evaluation" / "g06_controlled_reproduction.csv",
        help="Caminho do CSV de saída.",
    )
    arguments = parser.parse_args()
    if arguments.repeats < 1:
        parser.error("--repeats deve ser pelo menos 1.")
    output_path = arguments.output
    if not output_path.is_absolute():
        output_path = ROOT / output_path
    return run(arguments.repeats, output_path)


if __name__ == "__main__":
    raise SystemExit(main())
