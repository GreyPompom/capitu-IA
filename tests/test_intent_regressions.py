"""Regressões de linguagem para formulações bibliográficas gerais."""

import pytest

from app.chat_service import CapituChatService
from app.schemas import BookDetails, BookSummary, ChatRequest, ConversationState, Intent


class Catalog:
    def __init__(self) -> None:
        self.calls: list[tuple[str, str]] = []

    def search_by_title(self, value: str) -> list[BookSummary]:
        self.calls.append(("title", value))
        return [self._book("/works/OL1003134W", value)]

    def search_by_author(self, value: str) -> list[BookSummary]:
        self.calls.append(("author", value))
        return [self._book("/works/OL1003134W", "Obra de teste")]

    def search_by_subject(self, value: str) -> list[BookSummary]:
        self.calls.append(("subject", value))
        return [self._book("/works/OL1003134W", "Obra de teste")]

    def get_details(self, key: str, *, fallback_authors: tuple[str, ...] = ()) -> BookDetails:
        self.calls.append(("details", key))
        return BookDetails(
            openlibrary_key=key,
            title="O Hobbit",
            authors=list(fallback_authors) or ["Autor de teste"],
            isbn=["9780000000000"],
            source_url=f"https://openlibrary.org{key}",
        )

    @staticmethod
    def _book(key: str, title: str) -> BookSummary:
        return BookSummary(
            openlibrary_key=key,
            title=title,
            authors=["Autor de teste"],
            source_url=f"https://openlibrary.org{key}",
        )


@pytest.mark.parametrize(
    ("message", "intent", "call"),
    [
        ("Na lista, quero ver se consta Persépolis.", Intent.SEARCH_TITLE, ("title", "Persépolis")),
        ("Verifique se há algum registro de O Conto da Aia.", Intent.SEARCH_TITLE, ("title", "O Conto da Aia")),
        ("É pelo título “Grande Sertão: Veredas” que eu gostaria de pesquisar.", Intent.SEARCH_TITLE, ("title", "Grande Sertão: Veredas")),
        ("Quero conhecer as obras publicadas por Lygia Fagundes Telles.", Intent.SEARCH_AUTHOR_WORKS, ("author", "Lygia Fagundes Telles")),
        ("Queria indicações de fantasia", Intent.SEARCH_SUBJECT, ("subject", "fantasia")),
    ],
)
def test_general_bibliographic_variations_reach_the_right_catalog_operation(message, intent, call) -> None:
    catalog = Catalog()
    response = CapituChatService(catalog=catalog).handle(ChatRequest(message=message))

    assert response.intent is intent
    assert response.state is ConversationState.ANSWERED
    assert catalog.calls == [call]


def test_plural_isbns_is_recognized_as_book_details() -> None:
    catalog = Catalog()
    response = CapituChatService(catalog=catalog).handle(
        ChatRequest(message="Quais ISBNs constam para as edições de O Hobbit?")
    )

    assert response.intent is Intent.BOOK_DETAILS
    assert response.state is ConversationState.ANSWERED
    assert catalog.calls == [("title", "O Hobbit"), ("details", "/works/OL1003134W")]
