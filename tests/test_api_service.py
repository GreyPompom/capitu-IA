"""Testes das respostas controladas da Open Library, sem chamadas de rede."""

import json
import re
from pathlib import Path

import pytest


FIXTURES_DIR = Path(__file__).parent / "fixtures"


@pytest.fixture
def load_response():
    """Disponibiliza a leitura dos JSONs controlados da G03."""

    def load(filename: str) -> dict:
        path = FIXTURES_DIR / filename
        with path.open(encoding="utf-8") as fixture_file:
            response = json.load(fixture_file)

        assert isinstance(response, dict)
        return response

    return load


@pytest.mark.parametrize(
    ("filename", "expected_records"),
    [
        (
            "search_single.json",
            [
                (
                    "/works/OL1810404W",
                    "Quarto de Despejo",
                    ["Carolina Maria de Jesus"],
                )
            ],
        ),
        (
            "search_multiple.json",
            [
                (
                    "/works/OL1810404W",
                    "Quarto de Despejo",
                    ["Carolina Maria de Jesus"],
                ),
                (
                    "/works/OL1003134W",
                    "O Alienista",
                    ["Machado de Assis"],
                ),
                (
                    "/works/OL103123W",
                    "Fahrenheit 451",
                    ["Ray Bradbury"],
                ),
            ],
        ),
        ("search_empty.json", []),
        (
            "search_missing_fields.json",
            [("/works/OL7058886W", "O Cortiço", None)],
        ),
    ],
)
def test_search_response_format(load_response, filename, expected_records):
    """Confere contagem, formato e registros esperados em cada cenário."""
    response = load_response(filename)

    assert type(response["numFound"]) is int
    assert type(response["start"]) is int
    assert response["start"] == 0
    assert isinstance(response["docs"], list)
    assert response["numFound"] == len(expected_records)
    assert len(response["docs"]) == len(expected_records)

    keys = [book["key"] for book in response["docs"]]
    assert len(keys) == len(set(keys))

    for book, expected in zip(response["docs"], expected_records):
        expected_key, expected_title, expected_authors = expected

        assert book["key"] == expected_key
        assert re.fullmatch(r"/works/OL\d+W", book["key"])
        assert book["title"] == expected_title

        if expected_authors is None:
            assert "author_name" not in book
        else:
            assert isinstance(book["author_name"], list)
            assert book["author_name"] == expected_authors

        if "first_publish_year" in book:
            assert type(book["first_publish_year"]) is int
            assert 0 <= book["first_publish_year"] <= 9_999


def test_missing_fields_are_intentionally_absent(load_response):
    """Preserva a ausência de campos opcionais no exemplo de O Cortiço."""
    response = load_response("search_missing_fields.json")
    book = response["docs"][0]

    assert set(book) == {"key", "title"}


def test_edition_preserves_work_reference_and_publication_date(load_response):
    """Distingue a edição de Quarto de Despejo da primeira publicação da obra."""
    edition = load_response("edition.json")
    work = load_response("search_single.json")["docs"][0]

    assert edition["key"] == "/books/OL46864874M"
    assert re.fullmatch(r"/books/OL\d+M", edition["key"])
    assert edition["works"] == [{"key": work["key"]}]
    assert edition["title"] == work["title"]

    assert edition["publishers"] == ["Atica"]
    assert type(edition["number_of_pages"]) is int
    assert edition["number_of_pages"] == 202

    assert edition["isbn_10"] == ["8508105312"]
    assert edition["isbn_13"] == ["9788508105311"]

    assert edition["publish_date"] == "1993"
    assert work["first_publish_year"] == 1960
    assert "first_publish_year" not in edition