"""E2E controlado da E09: PLN, diálogo, catálogo simulado e resposta."""

from uuid import uuid4

import pytest

from app.chat_service import CapituChatService
from app.schemas import BookDetails, BookSummary, ChatRequest, ConversationState, Intent
from services.open_library import OpenLibraryUnavailableError


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
        title = "Segundo" if openlibrary_key == "/works/OL103123W" else "Dom Casmurro"
        return details(openlibrary_key, title, list(fallback_authors) or ["Machado de Assis"])


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


def test_author_list_command_uses_only_the_author_name() -> None:
    service, catalog = make_service()

    response = service.handle(ChatRequest(message="Obras do autor: me liste as obras de machado de assis"))

    assert response.intent is Intent.SEARCH_AUTHOR_WORKS
    assert response.state is ConversationState.ANSWERED
    assert catalog.calls == [("author", "machado de assis")]


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


def test_card_detail_command_runs_full_controlled_detail_flow() -> None:
    service, catalog = make_service()

    response = service.handle(ChatRequest(message="Consultar detalhes do livro: Dom Casmurro"))

    assert response.intent is Intent.BOOK_DETAILS
    assert response.state is ConversationState.ANSWERED
    assert catalog.calls == [("title", "Dom Casmurro"), ("details", "/works/OL1003134W")]
    assert response.results[0].title == "Dom Casmurro"


def test_summary_request_runs_controlled_detail_flow() -> None:
    service, catalog = make_service()

    response = service.handle(ChatRequest(message="quero ler o livro O pequeno principe, me de um resumo"))

    assert response.intent is Intent.BOOK_DETAILS
    assert response.state is ConversationState.ANSWERED
    assert catalog.calls == [("title", "O pequeno principe"), ("details", "/works/OL1003134W")]
    assert "Descrição" in response.text


def test_summary_with_interpretive_question_returns_description_and_scope_notice() -> None:
    service, catalog = make_service()

    response = service.handle(
        ChatRequest(message="quero um resumo sobre o livro O pequeno principe, quem era a rosa?")
    )

    assert response.intent is Intent.BOOK_DETAILS
    assert response.state is ConversationState.ANSWERED
    assert "Registro controlado para teste." in response.text
    assert "não respondo perguntas interpretativas" in response.text
    assert catalog.calls == [("title", "O pequeno principe"), ("details", "/works/OL1003134W")]


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
    assert [book.title for book in selected.results] == ["Segundo"]
    assert detail.intent is Intent.BOOK_DETAILS
    assert ("details", "/works/OL103123W") in catalog.calls


def test_detail_candidates_can_be_selected_without_repeating_the_title() -> None:
    service, catalog = make_service()
    catalog.title_results = [
        book("/works/OL1003134W", "Primeiro", ["Autor 1"]),
        book("/works/OL103123W", "Segundo", ["Autor 2"]),
    ]
    session_id = uuid4()

    initial = service.handle(ChatRequest(message="Consultar detalhes do livro: Memórias Póstumas de Brás Cubas", session_id=session_id))
    selected = service.handle(ChatRequest(message="o segundo", session_id=session_id))
    detail = service.handle(ChatRequest(message="Me dê um resumo", session_id=session_id))

    assert initial.state is ConversationState.AWAITING_SELECTION
    assert selected.state is ConversationState.ANSWERED
    assert [book.title for book in selected.results] == ["Segundo"]
    assert detail.state is ConversationState.ANSWERED
    assert detail.results[0].title == "Segundo"
    assert catalog.calls == [
        ("title", "Memórias Póstumas de Brás Cubas"),
        ("details", "/works/OL103123W"),
    ]


def test_summary_about_selected_work_uses_context_without_new_title_search() -> None:
    service, catalog = make_service()
    session_id = uuid4()

    service.handle(ChatRequest(message="Procure Dom Casmurro", session_id=session_id))
    response = service.handle(ChatRequest(message="me dê um resumo sobre a obra", session_id=session_id))

    assert response.intent is Intent.BOOK_DETAILS
    assert response.state is ConversationState.ANSWERED
    assert response.results[0].title == "Dom Casmurro"
    assert catalog.calls == [("title", "Dom Casmurro"), ("details", "/works/OL1003134W")]


def test_year_question_reuses_first_publication_year_from_selected_result() -> None:
    service, catalog = make_service()
    catalog.title_results = [catalog.title_results[0].model_copy(update={"first_publish_year": 1881})]

    def details_without_year(key: str, *, fallback_authors: tuple[str, ...] = ()) -> BookDetails:
        catalog.calls.append(("details", key))
        return BookDetails(
            openlibrary_key=key,
            title="Dom Casmurro",
            authors=list(fallback_authors),
            source_url=f"https://openlibrary.org{key}",
        )

    catalog.get_details = details_without_year
    session_id = uuid4()

    service.handle(ChatRequest(message="Procure Dom Casmurro", session_id=session_id))
    response = service.handle(ChatRequest(message="Em que ano este livro foi lançado?", session_id=session_id))

    assert response.intent is Intent.BOOK_DETAILS
    assert response.state is ConversationState.ANSWERED
    assert "Primeira publicação" in response.text
    assert "1881" in response.text


def test_short_author_question_uses_selected_book_context() -> None:
    service, catalog = make_service()
    session_id = uuid4()

    service.handle(ChatRequest(message="Procure Dom Casmurro", session_id=session_id))
    response = service.handle(ChatRequest(message="Qual autor?", session_id=session_id))

    assert response.intent is Intent.BOOK_DETAILS
    assert response.state is ConversationState.ANSWERED
    assert "Machado de Assis" in response.text
    assert catalog.calls == [("title", "Dom Casmurro"), ("details", "/works/OL1003134W")]


@pytest.mark.parametrize(
    ("message", "expected_fragment"),
    [
        ("Quem é o escritor?", "Machado de Assis"),
        ("Quando foi lançado?", "1899"),
        ("Mostre a sinopse", "Registro controlado para teste."),
        ("Qual editora?", "não forneceu esse campo"),
        ("Quais são os assuntos?", "não forneceu esse campo"),
    ],
)
def test_contextual_detail_field_variants_use_selected_book(message: str, expected_fragment: str) -> None:
    service, catalog = make_service()
    session_id = uuid4()

    service.handle(ChatRequest(message="Procure Dom Casmurro", session_id=session_id))
    response = service.handle(ChatRequest(message=message, session_id=session_id))

    assert response.intent is Intent.BOOK_DETAILS
    assert response.state is ConversationState.ANSWERED
    assert expected_fragment in response.text
    assert catalog.calls == [("title", "Dom Casmurro"), ("details", "/works/OL1003134W")]


def test_transient_catalog_failure_becomes_source_unavailable() -> None:
    service, catalog = make_service()

    def unavailable(_: str) -> list[BookSummary]:
        raise OpenLibraryUnavailableError("falha controlada")

    catalog.search_by_title = unavailable
    response = service.handle(ChatRequest(message="Procure Dom Casmurro"))

    assert response.state is ConversationState.SOURCE_UNAVAILABLE
    assert response.results == []
    assert "indisponível" in response.text
