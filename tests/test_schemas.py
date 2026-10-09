"""Testes unitários dos modelos Pydantic do contrato de chat v1."""

from uuid import UUID

import pytest
from pydantic import ValidationError

from app.schemas import (
    BookSummary,
    ChatMessage,
    ChatRequest,
    ChatResponse,
    ConversationSession,
    ConversationState,
    Intent,
    IntentCandidate,
    IntentDecision,
    IntentInterpretation,
)


def sample_book(number: int = 1) -> BookSummary:
    return BookSummary(
        openlibrary_key=f"/works/OL{number}W",
        title=f"Obra {number}",
        authors=["Autora Exemplo"],
        source_url=f"https://openlibrary.org/works/OL{number}W",
    )


def test_chat_request_accepts_message_without_existing_session() -> None:
    request = ChatRequest.model_validate({"message": "  Procure Dom Casmurro  "})

    assert request.message == "Procure Dom Casmurro"
    assert request.session_id is None


def test_internal_chat_message_accepts_only_user_or_assistant() -> None:
    assert ChatMessage(role="user", content="Oi").content == "Oi"
    with pytest.raises(ValidationError):
        ChatMessage(role="system", content="Instrução não permitida")


def test_business_intent_vocabulary_matches_the_four_planned_intents() -> None:
    assert {intent.value for intent in Intent} == {
        "buscar_por_titulo",
        "buscar_obras_autor",
        "buscar_por_assunto",
        "consultar_detalhes",
    }


@pytest.mark.parametrize("message", ["", "   ", "\n\t  "])
def test_chat_request_rejects_empty_or_whitespace_message(message: str) -> None:
    with pytest.raises(ValidationError):
        ChatRequest(message=message)


def test_chat_request_rejects_message_over_documented_limit() -> None:
    with pytest.raises(ValidationError):
        ChatRequest(message="x" * 1_001)


def test_chat_request_rejects_unexpected_fields_and_invalid_session_id() -> None:
    with pytest.raises(ValidationError):
        ChatRequest(message="Procure um livro", history=[])
    with pytest.raises(ValidationError):
        ChatRequest(message="Procure um livro", session_id="session-do-cliente")


def test_chat_response_has_text_state_session_id_and_result_list() -> None:
    response = ChatResponse(
        session_id=UUID("6f301173-2ec2-4c96-b58e-c9dc6dc2fc7b"),
        text="Encontrei um registro.",
        state=ConversationState.ANSWERED,
        intent=Intent.SEARCH_TITLE,
        results=[sample_book()],
    )

    payload = response.model_dump(mode="json")
    assert payload["text"] == "Encontrei um registro."
    assert payload["state"] == "answered"
    assert payload["session_id"] == "6f301173-2ec2-4c96-b58e-c9dc6dc2fc7b"
    assert isinstance(payload["results"], list)
    assert payload["results"][0]["title"] == "Obra 1"


def test_chat_response_defaults_results_to_empty_list() -> None:
    response = ChatResponse(
        session_id=UUID("6f301173-2ec2-4c96-b58e-c9dc6dc2fc7b"),
        text="Qual é o título?",
        state=ConversationState.AWAITING_CLARIFICATION,
        intent=Intent.SEARCH_TITLE,
    )

    assert response.results == []


def test_response_rejects_more_than_five_books() -> None:
    with pytest.raises(ValidationError):
        ChatResponse(
            session_id=UUID("6f301173-2ec2-4c96-b58e-c9dc6dc2fc7b"),
            text="Encontrei vários resultados.",
            state=ConversationState.AWAITING_SELECTION,
            results=[sample_book(i) for i in range(1, 7)],
        )


def test_interpretation_requires_intent_only_for_accepted_decision() -> None:
    accepted = IntentInterpretation(
        decision=IntentDecision.ACCEPTED,
        intent=Intent.SEARCH_AUTHOR_WORKS,
        similarity_score=0.74,
        margin=0.19,
        candidates=[IntentCandidate(intent=Intent.SEARCH_AUTHOR_WORKS, rank=1, similarity_score=0.74)],
    )

    assert accepted.intent is Intent.SEARCH_AUTHOR_WORKS
    with pytest.raises(ValidationError):
        IntentInterpretation(decision=IntentDecision.AMBIGUOUS, intent=Intent.SEARCH_TITLE)
    with pytest.raises(ValidationError):
        IntentInterpretation(decision=IntentDecision.ACCEPTED)


def test_similarity_score_is_not_allowed_outside_cosine_range() -> None:
    with pytest.raises(ValidationError):
        IntentCandidate(intent=Intent.SEARCH_TITLE, rank=1, similarity_score=1.01)


def test_session_keeps_only_bounded_pending_context_and_results() -> None:
    session = ConversationSession(
        state=ConversationState.AWAITING_SELECTION,
        last_results=[sample_book(i) for i in range(1, 6)],
    )

    assert isinstance(session.session_id, UUID)
    assert len(session.last_results) == 5
    assert "history" not in ConversationSession.model_fields
    with pytest.raises(ValidationError):
        ConversationSession(last_results=[sample_book(i) for i in range(1, 7)])
