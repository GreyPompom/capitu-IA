"""Avalia a CAPITU no split de teste sem usar esse split para ajuste."""

from __future__ import annotations

import csv
import hashlib
import json
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.schemas import Intent, IntentDecision
from evaluation.intent_metrics import FALLBACK_LABEL, calculate_intent_metrics, exact_match_rate
from nlp.entity_extraction import extract_entities
from nlp.intent_similarity import build_reference_index
from nlp.interpretation import interpret_message
from dialogue.policy import IntentDecisionPolicy


TEST_SPLIT = ROOT / "data" / "splits" / "test.csv"
NEGATIVE_DATA = ROOT / "data" / "Fora_Do_Escopo_Ambiguo.csv"
OUTPUT = ROOT / "evaluation" / "results" / "e11_intent_metrics.json"


def _rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as source:
        return list(csv.DictReader(source))


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _slot(intent: Intent) -> str:
    return {
        Intent.SEARCH_TITLE: "title",
        Intent.SEARCH_AUTHOR_WORKS: "author",
        Intent.SEARCH_SUBJECT: "subject",
        Intent.BOOK_DETAILS: "title",
    }[intent]


def _normalized(value: str | None) -> str:
    return " ".join((value or "").casefold().split())


def _canonical_requested_field(value: str) -> str:
    """Converte o rótulo curado do CSV para o contrato interno da CAPITU."""

    aliases = {
        "isbn": "isbn",
        "quantidade_edicoes": "edition_count",
        "numero_edicoes": "edition_count",
        "editora": "publisher",
        "descricao": "description",
        "resumo": "description",
        "assunto": "subjects",
        "ano": "first_publish_year",
        "autor": "author",
    }
    normalized = _normalized(value)
    return aliases.get(normalized, normalized)


def evaluate() -> dict[str, object]:
    """Executa avaliação final, sem rede e com índice treinado só na referência."""

    index = build_reference_index()
    policy = IntentDecisionPolicy()
    positive_rows = _rows(TEST_SPLIT)
    expected: list[str] = []
    predicted: list[str] = []
    entity_expected: list[str] = []
    entity_observed: list[str] = []
    field_expected: list[str] = []
    field_observed: list[str] = []
    contextual_parameter_rows: list[str] = []
    predictions: list[dict[str, object]] = []

    for row in positive_rows:
        intent = Intent(row["intencao"])
        result = interpret_message(row["texto"], index, policy)
        interpretation = result.interpretation
        observed_intent = (
            interpretation.intent.value
            if interpretation.decision is IntentDecision.ACCEPTED and interpretation.intent is not None
            else FALLBACK_LABEL
        )
        expected.append(intent.value)
        predicted.append(observed_intent)

        extraction = extract_entities(row["texto"], intent).entities
        entity = row.get("entidade", "")
        is_contextual = intent is Intent.BOOK_DETAILS and entity.casefold().startswith(("indice", "índice"))
        if entity and not is_contextual:
            entity_expected.append(_normalized(entity))
            entity_observed.append(_normalized(getattr(extraction, _slot(intent))))
        elif is_contextual:
            contextual_parameter_rows.append(row["id"])
        field = row.get("campo_solicitado", "")
        if field:
            field_expected.append(_canonical_requested_field(field))
            field_observed.append(extraction.requested_field or "")

        predictions.append(
            {
                "id": row["id"],
                "expected_intent": intent.value,
                "predicted_intent": observed_intent,
                "decision": interpretation.decision.value,
                "similarity_score": interpretation.similarity_score,
                "margin": interpretation.margin,
            }
        )

    negative_rows = _rows(NEGATIVE_DATA)
    negative_correct = 0
    negative_details: list[dict[str, str]] = []
    for row in negative_rows:
        result = interpret_message(row["entrada"], index, policy).interpretation
        observed_state = (
            "out_of_scope"
            if result.decision is IntentDecision.OUT_OF_SCOPE
            else "awaiting_clarification"
        )
        correct = observed_state == row["estado_esperado"]
        negative_correct += correct
        negative_details.append(
            {
                "id": row["id"],
                "expected_state": row["estado_esperado"],
                "observed_state": observed_state,
                "decision": result.decision.value,
                "correct": str(correct).lower(),
            }
        )

    return {
        "task": "E11",
        "executed_on": date.today().isoformat(),
        "mode": "offline_controlled_no_network",
        "training_source": str((ROOT / "data" / "splits" / "reference.csv").relative_to(ROOT)),
        "training_source_sha256": index.source_sha256,
        "test_source": str(TEST_SPLIT.relative_to(ROOT)),
        "test_source_sha256": _sha256(TEST_SPLIT),
        "test_split_used_for_training": False,
        "intent_metrics": calculate_intent_metrics(expected, predicted),
        "entity_exact_match": exact_match_rate(entity_expected, entity_observed),
        "requested_field_exact_match": exact_match_rate(field_expected, field_observed),
        "contextual_parameter_rows_excluded_from_direct_entity_metric": contextual_parameter_rows,
        "negative_behavior": {
            "total": len(negative_rows),
            "correct": negative_correct,
            "accuracy": negative_correct / len(negative_rows),
            "rows": negative_details,
        },
        "predictions": predictions,
    }


def main() -> int:
    results = evaluate()
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(results, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    metrics = results["intent_metrics"]
    print(
        f"E11: {metrics['correct']}/{metrics['total']} intenções corretas; "
        f"fallback={metrics['fallback_count']}/{metrics['total']}; resultado={OUTPUT.relative_to(ROOT)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
