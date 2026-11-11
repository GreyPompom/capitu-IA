"""Casos simples da G05 pelo TestClient, seguindo o padrão HTTP da E02."""

import pytest
from fastapi.testclient import TestClient

import app.main as main_module
from app.chat_service import CapituChatService
from app.schemas import BookDetails, BookSummary, Intent


class ControlledCatalog:
    def __init__(self) -> None:
        self.calls: list[tuple[str, str]] = []

    @staticmethod
    def book(key: str, title: str, authors: list[str]) -> BookSummary:
        return BookSummary(
            openlibrary_key=key,
            title=title,
            authors=authors,
            source_url=f"https://openlibrary.org{key}",
        )

    def search_by_title(self, title: str) -> list[BookSummary]:
        self.calls.append(("title", title))
        return [self.book("/works/OL1003134W", "Dom Casmurro", ["Machado de Assis"])]

    def search_by_author(self, author: str) -> list[BookSummary]:
        self.calls.append(("author", author))
        return [self.book("/works/OL1003134W", "Dom Casmurro", [author])]

    def search_by_subject(self, subject: str) -> list[BookSummary]:
        self.calls.append(("subject", subject))
        return [self.book("/works/OL103123W", "Fahrenheit 451", ["Ray Bradbury"])]

    def get_details(
        self,
        openlibrary_key: str,
        *,
        fallback_authors: tuple[str, ...] = (),
    ) -> BookDetails:
        raise AssertionError("Estes casos simples não devem solicitar detalhes.")


@pytest.mark.parametrize(
    ("message", "expected_intent", "expected_call"),
    [
        ("Procure Dom Casmurro", Intent.SEARCH_TITLE, ("title", "Dom Casmurro")),
        (
            "Quais livros Machado de Assis escreveu?",
            Intent.SEARCH_AUTHOR_WORKS,
            ("author", "Machado de Assis"),
        ),
        (
            "Quero livros sobre inteligência artificial",
            Intent.SEARCH_SUBJECT,
            ("subject", "inteligência artificial"),
        ),
    ],
)
def test_g05_simple_searches_use_e02_http_template(
    monkeypatch,
    message: str,
    expected_intent: Intent,
    expected_call: tuple[str, str],
) -> None:
    catalog = ControlledCatalog()
    monkeypatch.setattr(main_module, "chat_service", CapituChatService(catalog=catalog))
    client = TestClient(main_module.app)

    response = client.post("/api/chat", json={"message": message})

    assert response.status_code == 200
    body = response.json()
    assert body["intent"] == expected_intent.value
    assert body["results"]
    assert catalog.calls == [expected_call]
