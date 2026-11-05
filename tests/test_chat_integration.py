"""E2E controlado da E09: PLN, diálogo, catálogo simulado e resposta."""

from uuid import uuid4

from app.chat_service import CapituChatService
from app.schemas import BookDetails, BookSummary, ChatRequest, ConversationState, Intent


def book(key: str, title: str, authors: list[str]) -> BookSummary:
    return BookSummary(openlibrary_key=key, title=title, authors=authors, source_url=f"https://openlibrary.org{key}")


def details(key: str, title: str, authors: list[str]) -> BookDetails:
    return BookDetails(
        openlibrary_key=key,
        title=title,
        authors=authors,
        first_publish_year=1899,
        source_url=f"https://openlibrary.org{key}",
        description="Registro controlado para teste.",
    )


class FakeCatalog:
    def __init__(self) -> None:
        self.calls: list[tuple[str, str]] = []
        self.title_results = [book("/works/OL1003134W", "Dom Casmurro", ["Machado de Assis"])]
        self.author_results = [book("/works/OL1003134W", "Dom Casmurro", ["Machado de Assis"])]
        self.subject_results = [book("/works/OL103123W", "Fahrenheit 451", ["Ray Bradbury"])]

    def search_by_title(self, title: str) -> list[BookSummary]:
        self.calls.append(("title", title))
        return self.title_results

    def search_by_author(self, author: str) -> list[BookSummary]:
        self.calls.append(("author", author))
        return self.author_results

    def search_by_subject(self, subject: str) -> list[BookSummary]:
        self.calls.append(("subject", subject))
        return self.subject_results

    def get_details(self, openlibrary_key: str, *, fallback_authors: tuple[str, ...] = ()) -> BookDetails:
        self.calls.append(("details", openlibrary_key))
        return details(openlibrary_key, "Dom Casmurro", list(fallback_authors) or ["Machado de Assis"])


def make_service() -> tuple[CapituChatService, FakeCatalog]:
    catalog = FakeCatalog()
    return CapituChatService(catalog=catalog), catalog


def test_title_search_runs_full_controlled_pipeline() -> None:
    service, catalog = make_service()

    response = service.handle(ChatRequest(message="Procure Dom Casmurro"))

    assert response.intent is Intent.SEARCH_TITLE
    assert response.state is ConversationState.ANSWERED
    assert response.results[0].title == "Dom Casmurro"
    assert catalog.calls == [("title", "Dom Casmurro")]
    assert "Open Library" in response.text


def test_author_search_is_not_treated_as_author_biography() -> None:
    service, catalog = make_service()

    response = service.handle(ChatRequest(message="Quais livros Machado de Assis escreveu?"))

    assert response.intent is Intent.SEARCH_AUTHOR_WORKS
    assert response.results[0].authors == ["Machado de Assis"]
    assert catalog.calls == [("author", "Machado de Assis")]


def test_subject_search_runs_with_extracted_subject() -> None:
    service, catalog = make_service()

    response = service.handle(ChatRequest(message="Mostre livros sobre ficção científica"))

    assert response.intent is Intent.SEARCH_SUBJECT
    assert response.results[0].title == "Fahrenheit 451"
    assert catalog.calls == [("subject", "ficção científica")]


def test_detail_search_uses_title_then_detail_and_returns_requested_field() -> None:
    service, catalog = make_service()

    response = service.handle(ChatRequest(message="Quem escreveu Dom Casmurro?"))

    assert response.intent is Intent.BOOK_DETAILS
    assert response.state is ConversationState.ANSWERED
    assert catalog.calls == [("title", "Dom Casmurro"), ("details", "/works/OL1003134W")]
    assert "Machado de Assis" in response.text
    assert "Fonte: Open Library" in response.text


def test_missing_title_asks_without_catalog_call_then_accepts_short_answer() -> None:
    service, catalog = make_service()
    session_id = uuid4()

    pending = service.handle(ChatRequest(message="Busque um livro", session_id=session_id))
    resolved = service.handle(ChatRequest(message="Dom Casmurro", session_id=session_id))

    assert pending.state is ConversationState.AWAITING_CLARIFICATION
    assert pending.results == []
    assert resolved.intent is Intent.SEARCH_TITLE
    assert catalog.calls == [("title", "Dom Casmurro")]


def test_multiple_results_then_selection_then_details_uses_same_session() -> None:
    service, catalog = make_service()
    catalog.title_results = [
        book("/works/OL1003134W", "Primeiro", ["Autor 1"]),
        book("/works/OL103123W", "Segundo", ["Autor 2"]),
    ]
    session_id = uuid4()

    initial = service.handle(ChatRequest(message="Procure títulos clássicos", session_id=session_id))
    selected = service.handle(ChatRequest(message="o segundo", session_id=session_id))
    detail = service.handle(ChatRequest(message="Quem escreveu?", session_id=session_id))

    assert initial.state is ConversationState.AWAITING_SELECTION
    assert selected.state is ConversationState.ANSWERED
    assert detail.intent is Intent.BOOK_DETAILS
    assert ("details", "/works/OL103123W") in catalog.calls
