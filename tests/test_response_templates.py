"""Testes de apresentação para campos bibliográficos opcionais."""

from app.schemas import BookDetails
from responses.templates import detail_text


def make_details(**changes) -> BookDetails:
    data = {
        "openlibrary_key": "/works/OL1003134W",
        "title": "Obra de teste",
        "source_url": "https://openlibrary.org/works/OL1003134W",
    }
    data.update(changes)
    return BookDetails(**data)


def test_year_request_uses_available_edition_date_without_claiming_first_publication() -> None:
    text = detail_text(make_details(publication_date="1957"), "first_publish_year")

    assert "não forneceu a primeira publicação" in text
    assert "1957" in text
    assert "data de publicação disponível" in text


def test_description_can_explain_interpretive_content_is_out_of_scope() -> None:
    text = detail_text(
        make_details(description="Descrição bibliográfica disponível."),
        "description",
        has_interpretive_content_question=True,
    )

    assert "Descrição bibliográfica disponível." in text
    assert "não respondo perguntas interpretativas" in text
