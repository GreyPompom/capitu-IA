"""Testes da E04 para TF-IDF, cosseno e fronteira de dados de treino."""

import csv
import unittest

from app.schemas import Intent
from nlp.intent_similarity import REFERENCE_SPLIT_PATH, IntentSimilarityIndex, build_reference_index
from nlp.preprocessing import normalize_text


def _split_ids(name: str) -> set[str]:
    with (REFERENCE_SPLIT_PATH.parent / f"{name}.csv").open(encoding="utf-8-sig", newline="") as source:
        return {row["id"] for row in csv.DictReader(source)}


class IntentSimilarityTests(unittest.TestCase):
    def test_normalization_is_deterministic_and_preserves_words(self) -> None:
        self.assertEqual(
            normalize_text("  TÍTULOS, sobre Educação-Inclusiva!  "),
            "titulos sobre educacao inclusiva",
        )
        self.assertEqual(normalize_text("Quem escreveu O Quinze?"), "quem escreveu o quinze")

    def test_unseen_phrases_receive_a_traceable_top_intent(self) -> None:
        index = build_reference_index()
        cases = [
            ("Quero localizar o livro A Hora da Estrela", Intent.SEARCH_TITLE),
            ("Mostre publicações de Clarice Lispector", Intent.SEARCH_AUTHOR_WORKS),
            ("Preciso de leituras sobre sustentabilidade urbana", Intent.SEARCH_SUBJECT),
            (
                "Quais informações bibliográficas estão disponíveis sobre Ensaio sobre a Cegueira?",
                Intent.BOOK_DETAILS,
            ),
        ]

        for message, expected_intent in cases:
            with self.subTest(message=message):
                candidates = index.rank(message)
                self.assertIs(candidates[0].intent, expected_intent)
                self.assertEqual(candidates[0].rank, 1)
                self.assertGreater(candidates[0].similarity_score, 0.0)
                self.assertLessEqual(candidates[0].similarity_score, 1.0)
                self.assertEqual([candidate.rank for candidate in candidates], [1, 2, 3])
                self.assertEqual(
                    candidates,
                    sorted(candidates, key=lambda candidate: (-candidate.similarity_score, candidate.intent.value)),
                )

    def test_unknown_vocabulary_returns_zero_scores_without_crashing(self) -> None:
        candidates = build_reference_index().rank("qxv blorb zzyzx")

        self.assertEqual(len(candidates), 3)
        self.assertTrue(all(candidate.similarity_score == 0.0 for candidate in candidates))

    def test_fitting_uses_reference_only_and_refuses_evaluation_splits(self) -> None:
        index = build_reference_index()
        reference_ids = _split_ids("reference")

        self.assertEqual(set(index.reference_ids), reference_ids)
        self.assertTrue(reference_ids.isdisjoint(_split_ids("validation")))
        self.assertTrue(reference_ids.isdisjoint(_split_ids("test")))
        with self.assertRaisesRegex(ValueError, "somente data/splits/reference.csv"):
            IntentSimilarityIndex().fit_from_csv(REFERENCE_SPLIT_PATH.parent / "test.csv")

    def test_index_keeps_source_metadata_for_reproducible_artifacts(self) -> None:
        index = build_reference_index()

        self.assertEqual(index.source_path, str(REFERENCE_SPLIT_PATH.resolve()))
        self.assertEqual(len(index.reference_ids), 84)
        self.assertTrue(index.source_sha256)
