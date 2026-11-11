"""Testes da E06 para regras de extração e informação faltante."""

import unittest

from app.schemas import EntitySlot, Intent
from nlp.entity_extraction import extract_entities


class EntityExtractionTests(unittest.TestCase):
    def test_title_search_removes_command_and_preserves_original_title(self) -> None:
        result = extract_entities("Estou tentando achar A Vida Invisível de Eurídice Gusmão.", Intent.SEARCH_TITLE)

        self.assertEqual(result.entities.title, "A Vida Invisível de Eurídice Gusmão")
        self.assertFalse(result.needs_clarification)

    def test_quoted_title_is_preserved(self) -> None:
        result = extract_entities("O título que anotei foi “Ensaio sobre a Cegueira”; consegue localizar?", Intent.SEARCH_TITLE)

        self.assertEqual(result.entities.title, "Ensaio sobre a Cegueira")

    def test_author_search_preserves_a_compound_name(self) -> None:
        result = extract_entities("Quais livros Machado de Assis escreveu?", Intent.SEARCH_AUTHOR_WORKS)

        self.assertEqual(result.entities.author, "Machado de Assis")
        self.assertFalse(result.missing_required)

    def test_author_list_is_not_confused_with_title_author_question(self) -> None:
        author_result = extract_entities("Mostre livros da Clarice Lispector", Intent.SEARCH_AUTHOR_WORKS)
        details_result = extract_entities("Quem escreveu Dom Casmurro?", Intent.BOOK_DETAILS)

        self.assertEqual(author_result.entities.author, "Clarice Lispector")
        self.assertEqual(details_result.entities.title, "Dom Casmurro")
        self.assertEqual(details_result.entities.requested_field, "author")

    def test_subject_keeps_words_after_sobre(self) -> None:
        result = extract_entities("Quero livros sobre inteligência artificial.", Intent.SEARCH_SUBJECT)

        self.assertEqual(result.entities.subject, "inteligência artificial")

    def test_details_extracts_requested_field_and_title(self) -> None:
        result = extract_entities("Qual editora publicou A Bolsa Amarela?", Intent.BOOK_DETAILS)

        self.assertEqual(result.entities.title, "A Bolsa Amarela")
        self.assertEqual(result.entities.requested_field, "publisher")

    def test_details_command_from_card_extracts_title(self) -> None:
        result = extract_entities("Consultar detalhes do livro: Dom Casmurro", Intent.BOOK_DETAILS)

        self.assertEqual(result.entities.title, "Dom Casmurro")
        self.assertFalse(result.needs_clarification)

    def test_detail_request_for_summary_extracts_title_and_description_field(self) -> None:
        result = extract_entities("quero ler o livro O pequeno principe, me de um resumo", Intent.BOOK_DETAILS)

        self.assertEqual(result.entities.title, "O pequeno principe")
        self.assertEqual(result.entities.requested_field, "description")
        self.assertFalse(result.needs_clarification)

    def test_summary_about_selected_work_does_not_treat_context_as_a_title(self) -> None:
        result = extract_entities("me dê um resumo sobre a obra", Intent.BOOK_DETAILS)

        self.assertIsNone(result.entities.title)
        self.assertEqual(result.entities.requested_field, "description")
        self.assertEqual(result.missing_required, (EntitySlot.TITLE,))

    def test_isbn_is_optional_but_normalized_when_explicit(self) -> None:
        result = extract_entities("Quais dados do ISBN 978-85-359-0277-5?", Intent.BOOK_DETAILS)

        self.assertEqual(result.entities.isbn, "9788535902775")
        self.assertFalse(result.missing_required)

    def test_missing_required_parameter_is_explicit(self) -> None:
        result = extract_entities("Procure um livro", Intent.SEARCH_TITLE)

        self.assertEqual(result.missing_required, (EntitySlot.TITLE,))
        self.assertTrue(result.needs_clarification)

    def test_two_quoted_titles_are_a_conflict(self) -> None:
        result = extract_entities("Compare “Dom Casmurro” e “Memórias Póstumas”.", Intent.BOOK_DETAILS)

        self.assertIn("multiple_titles", result.conflicts)
        self.assertTrue(result.needs_clarification)

    def test_author_and_subject_filter_is_explicit_conflict(self) -> None:
        result = extract_entities("Quero livros de George Orwell sobre política.", Intent.SEARCH_AUTHOR_WORKS)

        self.assertEqual(result.entities.author, "George Orwell sobre política")
        self.assertIn("author_and_subject", result.conflicts)


if __name__ == "__main__":
    unittest.main()
