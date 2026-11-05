"""Gera evidência reproduzível da calibração E05, sem abrir o teste final."""

from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
from pathlib import Path

from sklearn.metrics.pairwise import cosine_similarity

from app.schemas import Intent, IntentCandidate
from dialogue.policy import IntentDecisionPolicy, IntentPolicyConfig
from nlp.intent_similarity import ROOT, build_reference_index


VALIDATION_PATH = ROOT / "data" / "splits" / "validation.csv"
NEGATIVE_AMBIGUOUS_PATH = ROOT / "data" / "Fora_Do_Escopo_Ambiguo.csv"
DEFAULT_OUTPUT = ROOT / "evaluation" / "results" / "e05_validation_calibration.json"


def candidates_for(index, message: str, *, method: str) -> list[IntentCandidate]:
    """Produz ranking por vizinho ou pela média dos três melhores por intenção."""

    similarities = cosine_similarity(index.vectorizer.transform([message]), index.reference_matrix).ravel()
    per_intent: dict[Intent, list[float]] = defaultdict(list)
    for example, score in zip(index.reference_examples, similarities, strict=True):
        per_intent[example.intent].append(float(score))

    if method == "nearest_neighbor":
        scores = {intent: max(values) for intent, values in per_intent.items()}
    elif method == "top_3_mean":
        scores = {
            intent: sum(sorted(values, reverse=True)[:3]) / 3
            for intent, values in per_intent.items()
        }
    else:
        raise ValueError(f"Método desconhecido: {method}")

    ordered = sorted(scores.items(), key=lambda item: (-item[1], item[0].value))
    return [
        IntentCandidate(intent=intent, rank=rank, similarity_score=score)
        for rank, (intent, score) in enumerate(ordered[:3], start=1)
    ]


def evaluate_validation(index, method: str, policy: IntentDecisionPolicy | None = None) -> dict[str, object]:
    rows = _read_csv(VALIDATION_PATH)
    policy = policy or IntentDecisionPolicy()
    decisions: dict[str, int] = defaultdict(int)
    accepted_correct = 0
    accepted_incorrect = 0
    raw_correct = 0

    for row in rows:
        candidates = candidates_for(index, row["texto"], method=method)
        if candidates[0].intent.value == row["intencao"]:
            raw_correct += 1
        interpretation = policy.interpret(row["texto"], candidates)
        decisions[interpretation.decision.value] += 1
        if interpretation.intent:
            if interpretation.intent.value == row["intencao"]:
                accepted_correct += 1
            else:
                accepted_incorrect += 1

    return {
        "rows": len(rows),
        "raw_top_1_correct": raw_correct,
        "raw_top_1_accuracy": _ratio(raw_correct, len(rows)),
        "accepted_correct": accepted_correct,
        "accepted_incorrect": accepted_incorrect,
        "false_accept_rate_among_accepted": _ratio(accepted_incorrect, accepted_correct + accepted_incorrect),
        "decision_counts": dict(sorted(decisions.items())),
    }


def evaluate_known_non_positive_cases(index, method: str) -> dict[str, object]:
    rows = _read_csv(NEGATIVE_AMBIGUOUS_PATH)
    policy = IntentDecisionPolicy()
    matches = 0
    results: dict[str, int] = defaultdict(int)
    expected_by_type = {"fora_do_escopo": "out_of_scope", "ambiguo": "ambiguous"}

    for row in rows:
        decision = policy.interpret(row["entrada"], candidates_for(index, row["entrada"], method=method)).decision.value
        results[decision] += 1
        matches += decision == expected_by_type[row["tipo"]]

    return {"rows": len(rows), "expected_decision_matches": matches, "decision_counts": dict(sorted(results.items()))}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()

    index = build_reference_index()
    report = {
        "source": {
            "reference": str(index.source_path),
            "reference_sha256": index.source_sha256,
            "validation": str(VALIDATION_PATH),
            "known_negative_ambiguous": str(NEGATIVE_AMBIGUOUS_PATH),
            "test_split_used": False,
        },
        "policy": {
            "acceptance_threshold": IntentDecisionPolicy().config.acceptance_threshold,
            "ambiguity_margin": IntentDecisionPolicy().config.ambiguity_margin,
            "score_is_probability": False,
        },
        "methods": {
            method: {
                "validation": evaluate_validation(index, method),
                "known_negative_ambiguous": evaluate_known_non_positive_cases(index, method),
            }
            for method in ("nearest_neighbor", "top_3_mean")
        },
        "top_3_mean_threshold_trials": {
            str(threshold): evaluate_validation(
                index,
                "top_3_mean",
                IntentDecisionPolicy(IntentPolicyConfig(acceptance_threshold=threshold, ambiguity_margin=0.12)),
            )
            for threshold in (0.18, 0.20, 0.23, 0.25, 0.30)
        },
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))


def _read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as source:
        return list(csv.DictReader(source))


def _ratio(numerator: int, denominator: int) -> float | None:
    return round(numerator / denominator, 4) if denominator else None


if __name__ == "__main__":
    main()
