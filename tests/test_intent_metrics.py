"""Testes da E11: denominadores incluem erro e abstenção."""

from evaluation.intent_metrics import FALLBACK_LABEL, calculate_intent_metrics, exact_match_rate


def test_metrics_include_error_and_fallback_in_accuracy_and_matrix() -> None:
    result = calculate_intent_metrics(
        ["buscar_por_titulo", "buscar_obras_autor", "buscar_por_assunto"],
        ["buscar_por_titulo", FALLBACK_LABEL, "buscar_por_titulo"],
    )

    assert result["total"] == 3
    assert result["correct"] == 1
    assert result["accuracy"] == 1 / 3
    assert result["fallback_count"] == 1
    assert result["fallback_rate"] == 1 / 3
    assert result["confusion_matrix"][-1] == [0, 0, 0, 0, 0]


def test_exact_match_rate_keeps_empty_denominator_explicit() -> None:
    assert exact_match_rate([], []) == {"total": 0, "correct": 0, "accuracy": None}
    assert exact_match_rate(["a", "b"], ["a", "x"]) == {"total": 2, "correct": 1, "accuracy": 0.5}
