from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

import app.main as main_module
from app.schemas import BookSummary, ChatResponse, ConversationState


@pytest.fixture
def client(monkeypatch):
    """Mantém os testes HTTP de contrato isolados da fonte externa real."""

    class ControlledService:
        def handle(self, request):
            return ChatResponse(
                session_id=request.session_id or uuid4(),
                text="Resposta controlada do contrato E09.",
                state=ConversationState.ANSWERED,
                intent=None,
                results=[
                    BookSummary(
                        openlibrary_key="/works/OL1003134W",
                        title="Dom Casmurro",
                        authors=["Machado de Assis"],
                        source_url="https://openlibrary.org/works/OL1003134W",
                    )
                ],
            )

    monkeypatch.setattr(main_module, "chat_service", ControlledService())
    return TestClient(main_module.app)


def test_chat_returns_contract_with_controlled_book_and_preserves_session(client) -> None:
    session_id = uuid4()

    response = client.post(
        "/api/chat",
        json={"message": "Quero livros sobre ficção científica", "session_id": str(session_id)},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["session_id"] == str(session_id)
    assert body["state"] == "answered"
    assert body["text"]
    assert isinstance(body["results"], list)
    assert len(body["results"]) == 1
    assert body["results"][0]["title"] == "Dom Casmurro"
    assert body["intent"] is None


def test_chat_creates_session_when_session_id_is_omitted(client) -> None:
    response = client.post("/api/chat", json={"message": "Buscar Dom Casmurro"})

    assert response.status_code == 200
    UUID(response.json()["session_id"])


def test_chat_rejects_empty_message_with_422(client) -> None:
    response = client.post("/api/chat", json={"message": "   "})

    assert response.status_code == 422


def test_chat_rejects_message_over_contract_limit_with_422(client) -> None:
    response = client.post("/api/chat", json={"message": "a" * 1_001})

    assert response.status_code == 422


def test_chat_rejects_invalid_session_id_with_422(client) -> None:
    response = client.post(
        "/api/chat",
        json={"message": "Buscar Dom Casmurro", "session_id": "not-a-uuid"},
    )

    assert response.status_code == 422


def test_root_serves_base_html_and_local_asset_references(client) -> None:
    response = client.get("/")

    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "CAPITU" in response.text
    assert "/static/styles.css" in response.text
    assert "/static/chat.js" in response.text


def test_static_assets_are_available_from_same_origin(client) -> None:
    css = client.get("/static/styles.css")
    javascript = client.get("/static/chat.js")

    assert css.status_code == 200
    assert "text/css" in css.headers["content-type"]
    assert "font-family" in css.text
    assert javascript.status_code == 200
    assert "javascript" in javascript.headers["content-type"]
