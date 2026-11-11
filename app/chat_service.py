"""Orquestra o fluxo completo da CAPITU sem acoplar regras ao endpoint HTTP."""

from __future__ import annotations

from typing import Protocol
from uuid import uuid4

from app.schemas import BookDetails, ChatRequest, ChatResponse, ConversationState, Intent
from dialogue.manager import DialogueManager
from dialogue.policy import IntentDecisionPolicy
from nlp.intent_similarity import IntentSimilarityIndex, build_reference_index
from nlp.interpretation import interpret_message
from responses.templates import detail_text, search_text, source_unavailable_text
from services.open_library import OpenLibraryClient, OpenLibraryUnavailableError


class CatalogClient(Protocol):
    def search_by_title(self, title: str): ...
    def search_by_author(self, author: str): ...
    def search_by_subject(self, subject: str): ...
    def get_details(self, openlibrary_key: str, *, fallback_authors: tuple[str, ...] = ()) -> BookDetails: ...


class CapituChatService:
    """Conecta interpretação, diálogo, catálogo e respostas de negócio."""

    def __init__(
        self,
        *,
        index: IntentSimilarityIndex | None = None,
        policy: IntentDecisionPolicy | None = None,
        dialogue: DialogueManager | None = None,
        catalog: CatalogClient | None = None,
    ) -> None:
        self.index = index or build_reference_index()
        self.policy = policy or IntentDecisionPolicy()
        self.dialogue = dialogue or DialogueManager()
        self.catalog = catalog or OpenLibraryClient()

    def handle(self, request: ChatRequest) -> ChatResponse:
        session_id = request.session_id or uuid4()
        interpreted = interpret_message(request.message, self.index, self.policy)
        outcome = self.dialogue.handle_interpretation(
            session_id,
            request.message,
            interpreted.interpretation,
            interpreted.extraction,
        )
        if not outcome.should_query or outcome.intent is None:
            return _response(outcome)

        try:
            if outcome.intent is Intent.BOOK_DETAILS:
                return self._handle_details(session_id, outcome)
            return self._handle_search(session_id, outcome)
        except OpenLibraryUnavailableError:
            unavailable = self.dialogue.record_source_unavailable(session_id)
            return _response(unavailable, text=source_unavailable_text())

    def _handle_search(self, session_id, outcome) -> ChatResponse:
        assert outcome.intent is not None
        if outcome.intent is Intent.SEARCH_TITLE:
            books = self.catalog.search_by_title(outcome.entities.title or "")
        elif outcome.intent is Intent.SEARCH_AUTHOR_WORKS:
            books = self.catalog.search_by_author(outcome.entities.author or "")
        elif outcome.intent is Intent.SEARCH_SUBJECT:
            books = self.catalog.search_by_subject(outcome.entities.subject or "")
        else:  # pragma: no cover - protegido pela chamada acima
            raise AssertionError("Intenção de busca inesperada")
        recorded = self.dialogue.record_search_results(session_id, outcome.intent, outcome.entities, books)
        return _response(
            recorded,
            text=search_text(outcome.intent, outcome.entities, books, recorded.session.state),
            intent=outcome.intent,
            entities=outcome.entities,
        )

    def _handle_details(self, session_id, outcome) -> ChatResponse:
        selected = outcome.selected_book
        if selected is None:
            # Uma consulta por título pode retornar mais de uma obra. Mantemos a
            # seleção explícita em vez de escolher a primeira arbitrariamente.
            matches = self.catalog.search_by_title(outcome.entities.title or "")
            recorded = self.dialogue.record_search_results(session_id, Intent.BOOK_DETAILS, outcome.entities, matches)
            if len(matches) != 1:
                return _response(
                    recorded,
                    text=search_text(Intent.SEARCH_TITLE, outcome.entities, matches, recorded.session.state),
                    intent=Intent.BOOK_DETAILS,
                    entities=outcome.entities,
                )
            selected = matches[0]

        details = self.catalog.get_details(selected.openlibrary_key, fallback_authors=tuple(selected.authors))
        # A busca pode trazer o ano da primeira publicação enquanto o payload
        # detalhado da mesma obra não o inclui. Reaproveitamos somente o dado
        # já fornecido pela fonte para a obra selecionada; não inferimos ano.
        if details.first_publish_year is None and selected.first_publish_year is not None:
            details = details.model_copy(update={"first_publish_year": selected.first_publish_year})
        recorded = self.dialogue.record_detail_result(session_id, details)
        return _response(
            recorded,
            text=detail_text(details, outcome.entities.requested_field),
            intent=Intent.BOOK_DETAILS,
            results=[details],
        )


def _response(outcome, *, text: str | None = None, intent: Intent | None = None, entities=None, results=None) -> ChatResponse:
    return ChatResponse(
        session_id=outcome.session.session_id,
        text=text or outcome.text,
        state=outcome.session.state,
        intent=intent if intent is not None else outcome.intent,
        results=outcome.session.last_results if results is None else results,
    )
