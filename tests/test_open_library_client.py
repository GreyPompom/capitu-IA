"""Testes da E08: cliente real com transporte HTTP controlado, sem rede."""

import json
from pathlib import Path

import httpx
import pytest

from services.open_library import (
    SEARCH_FIELDS,
    OpenLibraryClient,
    OpenLibraryUnavailableError,
)


FIXTURES_DIR = Path(__file__).parent / "fixtures"


def fixture(name: str) -> dict:
    return json.loads((FIXTURES_DIR / name).read_text(encoding="utf-8"))


def controlled_client(payloads: dict[str, dict], requests: list[httpx.Request] | None = None) -> OpenLibraryClient:
    seen = requests if requests is not None else []

    def handler(request: httpx.Request) -> httpx.Response:
        seen.append(request)
        payload = payloads.get(request.url.path)
        return httpx.Response(200, json=payload or {"docs": []}, request=request)

    transport = httpx.MockTransport(handler)
    return OpenLibraryClient(httpx.Client(transport=transport, base_url="https://openlibrary.org"))


def test_title_author_and_subject_use_expected_query_parameters() -> None:
    requests: list[httpx.Request] = []
    client = controlled_client({"/search.json": fixture("search_single.json")}, requests)

    client.search_by_title("  Quarto de   Despejo ")
    client.search_by_author("Carolina Maria de Jesus")
    client.search_by_subject("literatura brasileira")

    title_params, author_params, subject_params = [dict(request.url.params) for request in requests]
    assert title_params == {"title": "Quarto de Despejo", "limit": "5", "fields": SEARCH_FIELDS}
    assert author_params == {"author": "Carolina Maria de Jesus", "limit": "5", "fields": SEARCH_FIELDS}
    assert subject_params == {"q": "subject:literatura brasileira", "limit": "5", "fields": SEARCH_FIELDS}


def test_search_normalizes_multiple_authors_and_preserves_ids() -> None:
    client = controlled_client({"/search.json": fixture("search_multiple.json")})

    books = client.search_by_title("livros")

    assert [book.openlibrary_key for book in books] == [
        "/works/OL1810404W",
        "/works/OL1003134W",
        "/works/OL103123W",
    ]
    assert books[1].authors == ["Machado de Assis"]
    assert str(books[0].source_url) == "https://openlibrary.org/works/OL1810404W"


def test_missing_optional_search_fields_become_empty_or_null() -> None:
    client = controlled_client({"/search.json": fixture("search_missing_fields.json")})

    book = client.search_by_title("O Cortiço")[0]

    assert book.authors == []
    assert book.first_publish_year is None
    assert book.edition_count is None
    assert book.isbn == []
    assert book.subjects == []
    assert book.cover_url is None


def test_work_detail_preserves_work_date_description_and_author_id() -> None:
    client = controlled_client({"/works/OL1810404W.json": fixture("work.json")})

    details = client.get_details("/works/OL1810404W", fallback_authors=("Carolina Maria de Jesus",))

    assert details.openlibrary_key == "/works/OL1810404W"
    assert details.first_publish_year == 1960
    assert details.publication_date is None
    assert details.description == "Descrição controlada da obra."
    assert details.authors == ["Carolina Maria de Jesus"]
    assert details.author_keys == ["/authors/OL217145A"]
    assert details.subjects == ["Poor", "Social life and customs"]


def test_edition_detail_does_not_claim_first_publish_year() -> None:
    client = controlled_client({"/books/OL46864874M.json": fixture("edition.json")})

    details = client.get_details("/books/OL46864874M")

    assert details.openlibrary_key == "/books/OL46864874M"
    assert details.work_key == "/works/OL1810404W"
    assert details.first_publish_year is None
    assert details.publication_date == "1993"
    assert details.publishers == ["Atica"]
    assert details.isbn == ["9788508105311", "8508105312"]
    assert details.page_count == 202


def test_http_error_becomes_source_unavailable() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(503, json={"error": "temporarily unavailable"}, request=request)

    client = OpenLibraryClient(httpx.Client(transport=httpx.MockTransport(handler), base_url="https://openlibrary.org"))

    with pytest.raises(OpenLibraryUnavailableError):
        client.search_by_title("Duna")


def test_rejects_unknown_detail_key_without_http_request() -> None:
    client = controlled_client({})

    with pytest.raises(ValueError, match="chave de detalhe"):
        client.get_details("https://example.org/not-a-key")
