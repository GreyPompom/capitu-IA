"""Verificações estáticas do contrato entre a UI e o backend local."""

from pathlib import Path


CHAT_JS = (Path(__file__).resolve().parents[1] / "static" / "chat.js").read_text(encoding="utf-8")


def test_ui_uses_the_contract_route_and_session_fields() -> None:
    assert 'fetchWithTimeout("/api/chat"' in CHAT_JS
    assert "message: text, session_id: currentSessionId" in CHAT_JS
    assert "currentSessionId = data.session_id" in CHAT_JS
    assert "currentSessionId = null" in CHAT_JS


def test_card_uses_selection_for_ambiguous_results_and_details_otherwise() -> None:
    assert 'state === "awaiting_selection"' in CHAT_JS
    assert '"o segundo"' in CHAT_JS
    assert 'userInput.value = state === "awaiting_selection"' in CHAT_JS
    assert ': `Detalhes de “${title}”`' in CHAT_JS


def test_http_and_network_failures_have_distinct_messages() -> None:
    assert "class ChatHttpError" in CHAT_JS
    assert "O servidor não aceitou esta solicitação" in CHAT_JS
    assert "Não foi possível comunicar com o servidor" in CHAT_JS


def test_timeout_cancels_request_and_releases_the_ui_path() -> None:
    assert "const CHAT_REQUEST_TIMEOUT_MS = 15000" in CHAT_JS
    assert "class ChatTimeoutError" in CHAT_JS
    assert "new AbortController()" in CHAT_JS
    assert "Promise.race([request, timeout])" in CHAT_JS
    assert "controller.abort()" in CHAT_JS
    assert "window.clearTimeout(timeoutId)" in CHAT_JS
    assert "A consulta demorou mais do que o esperado" in CHAT_JS
