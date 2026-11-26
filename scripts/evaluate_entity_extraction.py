"""Mede a extração E06 somente na partição de referência, sem abrir o teste."""

from __future__ import annotations

import csv
import json
from pathlib import Path

from app.schemas import Intent
from nlp.entity_extraction import extract_entities


ROOT = Path(__file__).resolve().parents[1]
DATASET_PATH = ROOT / "data" / "splits" / "reference.csv"
DEFAULT_OUTPUT = ROOT / "evaluation" / "results" / "e06_entity_extraction_reference.json"
CONTEXT_ENTITIES = {"dessa edição", "segundo livro", "desse livro", "primeiro livro", "essa obra", "livro 3", "isso", "obra selecionada", "índice 2", "índice 3"}


def main() -> None:
    with DATASET_PATH.open(encoding="utf-8-sig", newline="") as source:
        rows = list(csv.DictReader(source))

    direct_total = direct_correct = context_total = context_missing = 0
    failures: list[dict[str, object]] = []
    for row in rows:
        intent = Intent(row["intencao"])
        result = extract_entities(row["texto"], intent)
        expected = row["entidade"]
        if expected in CONTEXT_ENTITIES:
            context_total += 1
            if result.missing_required:
                context_missing += 1
            else:
                failures.append({"id": row["id"], "expected": "pending context", "actual": result.entities.model_dump()})
            continue

        direct_total += 1
        actual = _primary_entity(intent, result.entities.model_dump())
        if actual == expected:
            direct_correct += 1
        else:
            failures.append({"id": row["id"], "expected": expected, "actual": actual, "input": row["texto"]})

    report = {
        "dataset": str(DATASET_PATH),
        "test_split_used": False,
        "direct_entity_exact_match": {"correct": direct_correct, "total": direct_total},
        "context_reference_needing_session": {"correctly_pending": context_missing, "total": context_total},
        "failures": failures,
    }
    DEFAULT_OUTPUT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))


def _primary_entity(intent: Intent, entities: dict[str, object]) -> object:
    if intent is Intent.SEARCH_TITLE or intent is Intent.BOOK_DETAILS:
        return entities["title"]
    if intent is Intent.SEARCH_AUTHOR_WORKS:
        return entities["author"]
    return entities["subject"]


if __name__ == "__main__":
    main()
