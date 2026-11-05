"""Testes unitários da E05: limiar, margem, ambiguidade e abstenção."""

import csv
from pathlib import Path
import unittest

from app.schemas import Intent, IntentCandidate, IntentDecision
from dialogue.policy import IntentDecisionPolicy, IntentPolicyConfig
from nlp.intent_similarity import ROOT, build_reference_index


def candidate(intent: Intent, rank: int, score: float) -> IntentCandidate:
    return IntentCandidate(intent=intent, rank=rank, similarity_score=score)


class IntentDecisionPolicyTests(unittest.TestCase):
    def setUp(self) -> None:
        self.policy = IntentDecisionPolicy(IntentPolicyConfig(acceptance_threshold=0.70, ambiguity_margin=0.12))

    def test_accepts_when_score_and_margin_are_sufficient(self) -> None:
        result = self.policy.interpret(
            "Quero localizar um livro",
            [
                candidate(Intent.SEARCH_TITLE, 1, 0.84),
                candidate(Intent.BOOK_DETAILS, 2, 0.31),
                candidate(Intent.SEARCH_SUBJECT, 3, 0.10),
            ],
        )

        self.assertEqual(result.decision, IntentDecision.ACCEPTED)
        self.assertEqual(result.intent, Intent.SEARCH_TITLE)
        self.assertAlmostEqual(result.margin or 0, 0.53)

    def test_default_parameters_are_the_calibrated_parameters(self) -> None:
        config = IntentDecisionPolicy().config

        self.assertEqual(config.acceptance_threshold, 0.25)
        self.assertEqual(config.ambiguity_margin, 0.12)

    def test_below_threshold_is_rejected_without_an_intent(self) -> None:
        result = self.policy.interpret(
            "Quero localizar algo",
            [candidate(Intent.SEARCH_TITLE, 1, 0.69), candidate(Intent.BOOK_DETAILS, 2, 0.20)],
        )

        self.assertEqual(result.decision, IntentDecision.REJECTED)
        self.assertIsNone(result.intent)

    def test_small_margin_is_ambiguous(self) -> None:
        result = self.policy.interpret(
            "Quero saber sobre uma obra",
            [candidate(Intent.SEARCH_TITLE, 1, 0.82), candidate(Intent.BOOK_DETAILS, 2, 0.75)],
        )

        self.assertEqual(result.decision, IntentDecision.AMBIGUOUS)
        self.assertIsNone(result.intent)

    def test_no_evidence_is_rejected(self) -> None:
        result = self.policy.interpret(
            "qxv blorb zzyzx",
            [candidate(Intent.SEARCH_TITLE, 1, 0.0), candidate(Intent.BOOK_DETAILS, 2, 0.0)],
        )

        self.assertEqual(result.decision, IntentDecision.REJECTED)
        self.assertIsNone(result.intent)

    def test_known_operational_request_has_scope_precedence(self) -> None:
        result = self.policy.interpret(
            "Renove meu empréstimo de Dom Casmurro.",
            [candidate(Intent.SEARCH_TITLE, 1, 0.91), candidate(Intent.BOOK_DETAILS, 2, 0.45)],
        )

        self.assertEqual(result.decision, IntentDecision.OUT_OF_SCOPE)
        self.assertIsNone(result.intent)

    def test_short_nominal_request_is_ambiguous_when_it_has_evidence(self) -> None:
        result = self.policy.interpret(
            "Machado",
            [candidate(Intent.SEARCH_AUTHOR_WORKS, 1, 0.33), candidate(Intent.SEARCH_TITLE, 2, 0.0)],
        )

        self.assertEqual(result.decision, IntentDecision.AMBIGUOUS)
        self.assertIsNone(result.intent)

    def test_curated_negative_and_ambiguous_cases_are_never_accepted(self) -> None:
        index = build_reference_index()
        expected_by_type = {"fora_do_escopo": IntentDecision.OUT_OF_SCOPE, "ambiguo": IntentDecision.AMBIGUOUS}
        path = ROOT / "data" / "Fora_Do_Escopo_Ambiguo.csv"
        with path.open(encoding="utf-8-sig", newline="") as source:
            rows = list(csv.DictReader(source))

        for row in rows:
            with self.subTest(case_id=row["id"]):
                result = self.policy.interpret(row["entrada"], index.rank(row["entrada"]))
                self.assertEqual(result.decision, expected_by_type[row["tipo"]])
                self.assertIsNone(result.intent)


if __name__ == "__main__":
    unittest.main()
