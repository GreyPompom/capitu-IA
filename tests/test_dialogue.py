"""Testes da E07 para contexto mínimo, pendência e seleção por sessão."""

from uuid import uuid4
import unittest

from app.schemas import (
    BookSummary,
    ConversationState,
    EntitySlot,
    ExtractedEntities,
    Intent,
    IntentDecision,
    IntentInterpretation,
)
from dialogue.manager import DialogueManager
from nlp.entity_extraction import EntityExtraction


def book(identifier: str, title: str) -> BookSummary:
    return BookSummary(
        openlibrary_key=f"/works/{identifier}",
        title=title,
        authors=["Autor de teste"],
        source_url=f"https://openlibrary.org/works/{identifier}",
    )


def accepted(intent: Intent, entities: ExtractedEntities | None = None) -> IntentInterpretation:
    return IntentInterpretation(decision=IntentDecision.ACCEPTED, intent=intent, entities=entities or ExtractedEntities())


def rejected() -> IntentInterpretation:
    return IntentInterpretation(decision=IntentDecision.REJECTED)


def out_of_scope() -> IntentInterpretation:
    return IntentInterpretation(decision=IntentDecision.OUT_OF_SCOPE)


class DialogueManagerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.manager = DialogueManager()

    def test_missing_parameter_then_short_answer_completes_pending_query(self) -> None:
        session_id = uuid4()
        start = self.manager.handle_interpretation(
            session_id,
            "Procure um livro",
            accepted(Intent.SEARCH_TITLE),
            EntityExtraction(entities=ExtractedEntities(), missing_required=(EntitySlot.TITLE,)),
        )
        self.assertEqual(start.session.state, ConversationState.AWAITING_CLARIFICATION)
        self.assertEqual(start.session.pending_intent, Intent.SEARCH_TITLE)
        self.assertFalse(start.should_query)

        follow_up = self.manager.handle_interpretation(session_id, "Dom Casmurro", rejected())
        self.assertTrue(follow_up.should_query)
        self.assertEqual(follow_up.intent, Intent.SEARCH_TITLE)
        self.assertEqual(follow_up.entities.title, "Dom Casmurro")
        self.assertEqual(follow_up.session.state, ConversationState.IDLE)

    def test_search_second_result_then_detail_uses_selected_book(self) -> None:
        session_id = uuid4()
        search_entities = ExtractedEntities(subject="ficção científica")
        self.manager.record_search_results(
            session_id,
            Intent.SEARCH_SUBJECT,
            search_entities,
            [book("A", "Primeiro"), book("B", "Segundo"), book("C", "Terceiro")],
        )

        selection = self.manager.handle_interpretation(session_id, "o segundo", rejected())
        self.assertEqual(selection.session.state, ConversationState.ANSWERED)
        self.assertEqual(selection.selected_book.openlibrary_key, "/works/B")

        details = self.manager.handle_interpretation(
            session_id,
            "Quem escreveu?",
            accepted(Intent.BOOK_DETAILS),
            EntityExtraction(entities=ExtractedEntities(requested_field="author"), missing_required=(EntitySlot.TITLE,)),
        )
        self.assertTrue(details.should_query)
        self.assertEqual(details.intent, Intent.BOOK_DETAILS)
        self.assertEqual(details.entities.title, "Segundo")
        self.assertEqual(details.selected_book.openlibrary_key, "/works/B")

    def test_invalid_selection_keeps_results_available(self) -> None:
        session_id = uuid4()
        self.manager.record_search_results(
            session_id,
            Intent.SEARCH_TITLE,
            ExtractedEntities(title="Duna"),
            [book("A", "Duna"), book("B", "Duna Messiah")],
        )

        outcome = self.manager.handle_interpretation(session_id, "o quarto", rejected())
        self.assertEqual(outcome.session.state, ConversationState.AWAITING_SELECTION)
        self.assertEqual(len(outcome.session.last_results), 2)
        self.assertIn("entre 1 e 2", outcome.text)

    def test_new_explicit_request_replaces_pending_context(self) -> None:
        session_id = uuid4()
        self.manager.handle_interpretation(
            session_id,
            "Procure um livro",
            accepted(Intent.SEARCH_TITLE),
            EntityExtraction(entities=ExtractedEntities(), missing_required=(EntitySlot.TITLE,)),
        )

        outcome = self.manager.handle_interpretation(
            session_id,
            "Quero livros sobre astronomia",
            accepted(Intent.SEARCH_SUBJECT),
            EntityExtraction(entities=ExtractedEntities(subject="astronomia")),
        )
        self.assertTrue(outcome.should_query)
        self.assertEqual(outcome.intent, Intent.SEARCH_SUBJECT)
        self.assertIsNone(outcome.session.pending_intent)
        self.assertEqual(outcome.entities.subject, "astronomia")

    def test_cancel_clears_only_its_own_session(self) -> None:
        first, second = uuid4(), uuid4()
        self.manager.record_search_results(first, Intent.SEARCH_TITLE, ExtractedEntities(title="Duna"), [book("A", "Duna")])
        self.manager.record_search_results(second, Intent.SEARCH_TITLE, ExtractedEntities(title="1984"), [book("B", "1984")])

        cancelled = self.manager.handle_interpretation(first, "cancelar", rejected())
        untouched = self.manager.store.get_or_create(second)
        self.assertEqual(cancelled.session.state, ConversationState.IDLE)
        self.assertEqual(cancelled.session.last_results, [])
        self.assertEqual(untouched.selected_book.title, "1984")

    def test_sessions_do_not_share_selection_context(self) -> None:
        first, second = uuid4(), uuid4()
        self.manager.record_search_results(first, Intent.SEARCH_TITLE, ExtractedEntities(title="Duna"), [book("A", "Duna"), book("B", "Duna Messiah")])

        outcome = self.manager.handle_interpretation(second, "o segundo", rejected())
        self.assertEqual(outcome.session.state, ConversationState.AWAITING_CLARIFICATION)
        self.assertIsNone(outcome.selected_book)

    def test_out_of_scope_never_requests_a_book_query(self) -> None:
        outcome = self.manager.handle_interpretation(uuid4(), "Qual a previsão do tempo?", out_of_scope())

        self.assertEqual(outcome.session.state, ConversationState.OUT_OF_SCOPE)
        self.assertFalse(outcome.should_query)


if __name__ == "__main__":
    unittest.main()
