"""Verificações estáticas do contrato entre a UI e o backend local."""

from pathlib import Path


CHAT_JS = (Path(__file__).resolve().parents[1] / "static" / "chat.js").read_text(encoding="utf-8")


def test_ui_uses_the_contract_route_and_session_fields() -> None:
    assert 'fetch("/api/chat"' in CHAT_JS
    assert "message: text, session_id: currentSessionId" in CHAT_JS
    assert "currentSessionId = data.session_id" in CHAT_JS
    assert "currentSessionId = null" in CHAT_JS


def test_card_uses_a_detail_prompt_that_preserves_the_title() -> None:
    assert 'userInput.value = `Detalhes de “${title}”`' in CHAT_JS


def test_http_and_network_failures_have_distinct_messages() -> None:
    assert "class ChatHttpError" in CHAT_JS
    assert "O servidor não aceitou esta solicitação" in CHAT_JS
    assert "Não foi possível comunicar com o servidor" in CHAT_JS
