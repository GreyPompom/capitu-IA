from uuid import UUID, uuid4

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_chat_returns_contract_with_simulated_book_and_preserves_session() -> None:
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
    assert "fictícios" in body["results"][0]["title"]
    assert body["intent"] is None


def test_chat_creates_session_when_session_id_is_omitted() -> None:
    response = client.post("/api/chat", json={"message": "Buscar Dom Casmurro"})

    assert response.status_code == 200
    UUID(response.json()["session_id"])


def test_chat_rejects_empty_message_with_422() -> None:
    response = client.post("/api/chat", json={"message": "   "})

    assert response.status_code == 422


def test_chat_rejects_message_over_contract_limit_with_422() -> None:
    response = client.post("/api/chat", json={"message": "a" * 1_001})

    assert response.status_code == 422


def test_chat_rejects_invalid_session_id_with_422() -> None:
    response = client.post(
        "/api/chat",
        json={"message": "Buscar Dom Casmurro", "session_id": "not-a-uuid"},
    )

    assert response.status_code == 422


def test_root_serves_base_html_and_local_asset_references() -> None:
    response = client.get("/")

    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "CAPITU" in response.text
    assert "/static/styles.css" in response.text
    assert "/static/chat.js" in response.text


def test_static_assets_are_available_from_same_origin() -> None:
    css = client.get("/static/styles.css")
    javascript = client.get("/static/chat.js")

    assert css.status_code == 200
    assert "text/css" in css.headers["content-type"]
    assert "font-family" in css.text
    assert javascript.status_code == 200
    assert "javascript" in javascript.headers["content-type"]
