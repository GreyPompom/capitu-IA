"""Métricas reproduzíveis para a avaliação offline da CAPITU."""

from __future__ import annotations

from collections.abc import Sequence

from sklearn.metrics import accuracy_score, classification_report, confusion_matrix


INTENT_LABELS = (
    "buscar_por_titulo",
    "buscar_obras_autor",
    "buscar_por_assunto",
    "consultar_detalhes",
)
FALLBACK_LABEL = "fallback"


def calculate_intent_metrics(expected: Sequence[str], predicted: Sequence[str]) -> dict[str, object]:
    """Calcula métricas sem ocultar abstenções entre os casos corretos."""

    if not expected or len(expected) != len(predicted):
        raise ValueError("As listas esperada e prevista devem ter o mesmo tamanho não vazio.")
    invalid_expected = set(expected).difference(INTENT_LABELS)
    invalid_predicted = set(predicted).difference((*INTENT_LABELS, FALLBACK_LABEL))
    if invalid_expected or invalid_predicted:
        raise ValueError("Há rótulos fora do contrato de avaliação.")

    labels_with_fallback = (*INTENT_LABELS, FALLBACK_LABEL)
    report = classification_report(
        expected,
        predicted,
        labels=INTENT_LABELS,
        target_names=INTENT_LABELS,
        output_dict=True,
        zero_division=0,
    )
    matrix = confusion_matrix(expected, predicted, labels=labels_with_fallback).tolist()
    fallback_count = sum(label == FALLBACK_LABEL for label in predicted)
    return {
        "total": len(expected),
        "correct": sum(actual == observed for actual, observed in zip(expected, predicted, strict=True)),
        "accuracy": accuracy_score(expected, predicted),
        "fallback_count": fallback_count,
        "fallback_rate": fallback_count / len(expected),
        "classification_report": report,
        "confusion_matrix_labels": list(labels_with_fallback),
        "confusion_matrix": matrix,
    }


def exact_match_rate(expected: Sequence[str], observed: Sequence[str]) -> dict[str, object]:
    """Calcula acerto exato para entidade ou campo solicitado."""

    if len(expected) != len(observed):
        raise ValueError("As listas esperada e observada precisam ter o mesmo tamanho.")
    if not expected:
        return {"total": 0, "correct": 0, "accuracy": None}
    correct = sum(item == result for item, result in zip(expected, observed, strict=True))
    return {"total": len(expected), "correct": correct, "accuracy": correct / len(expected)}
