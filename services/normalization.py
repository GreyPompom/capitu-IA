"""Conversão defensiva de payloads da Open Library em modelos internos."""

from __future__ import annotations

import re
from typing import Any, Iterable

from app.schemas import BookDetails, BookSummary


OPEN_LIBRARY_BASE_URL = "https://openlibrary.org"
COVERS_BASE_URL = "https://covers.openlibrary.org/b/id"


class OpenLibraryPayloadError(ValueError):
    """A fonte respondeu JSON, mas sem os campos mínimos para uso seguro."""


def normalize_search_document(document: dict[str, Any]) -> BookSummary:
    """Normaliza um item de `/search.json` sem inventar campos ausentes."""

    key = _required_key(document)
    title = _required_text(document, "title")
    return BookSummary(
        openlibrary_key=key,
        title=title,
        authors=_string_list(document.get("author_name"), limit=10),
        first_publish_year=_year(document.get("first_publish_year")),
        edition_count=_non_negative_int(document.get("edition_count")),
        isbn=_unique_strings(_iter_values(document.get("isbn")), limit=5),
        subjects=_string_list(document.get("subject"), limit=10),
        cover_url=_cover_url(document.get("cover_i")),
        source_url=_source_url(key),
    )


def normalize_detail_payload(
    payload: dict[str, Any],
    *,
    fallback_authors: Iterable[str] = (),
) -> BookDetails:
    """Normaliza obra ou edição preservando suas datas e referências próprias."""

    key = _required_key(payload)
    title = _required_text(payload, "title")
    author_names, author_keys = _detail_authors(payload.get("authors"))
    if not author_names:
        author_names = _unique_strings(fallback_authors, limit=10)
    work_key = _work_key(payload.get("works"))
    isbns = _unique_strings(
        [*_iter_values(payload.get("isbn_13")), *_iter_values(payload.get("isbn_10"))],
        limit=5,
    )
    description = _description(payload.get("description"))
    return BookDetails(
        openlibrary_key=key,
        title=title,
        authors=author_names,
        first_publish_year=_year(payload.get("first_publish_date")),
        edition_count=None,
        isbn=isbns,
        subjects=_string_list(payload.get("subjects"), limit=10),
        cover_url=_cover_url(_first(payload.get("covers"))),
        source_url=_source_url(key),
        description=description,
        publishers=_string_list(payload.get("publishers"), limit=10),
        publication_date=_optional_text(payload.get("publish_date")),
        work_key=work_key,
        author_keys=author_keys,
        page_count=_non_negative_int(payload.get("number_of_pages")),
    )


def _required_key(payload: dict[str, Any]) -> str:
    key = _optional_text(payload.get("key"))
    if not key or not re.fullmatch(r"/(?:works|books)/OL\d+[WM]", key):
        raise OpenLibraryPayloadError("A resposta não contém uma chave de obra/edição válida.")
    return key


def _required_text(payload: dict[str, Any], field: str) -> str:
    value = _optional_text(payload.get(field))
    if not value:
        raise OpenLibraryPayloadError(f"A resposta não contém {field!r} válido.")
    return value


def _optional_text(value: Any) -> str | None:
    return value.strip() if isinstance(value, str) and value.strip() else None


def _string_list(value: Any, *, limit: int) -> list[str]:
    return _unique_strings(_iter_values(value), limit=limit)


def _iter_values(value: Any) -> list[Any]:
    return value if isinstance(value, list) else ([] if value is None else [value])


def _unique_strings(values: Iterable[Any], *, limit: int) -> list[str]:
    unique: list[str] = []
    for value in values:
        text = _optional_text(value)
        if text and text not in unique:
            unique.append(text)
        if len(unique) == limit:
            break
    return unique


def _year(value: Any) -> int | None:
    if isinstance(value, int) and 0 <= value <= 9_999:
        return value
    if isinstance(value, str):
        match = re.search(r"\b(\d{4})\b", value)
        return int(match.group(1)) if match else None
    return None


def _non_negative_int(value: Any) -> int | None:
    return value if isinstance(value, int) and value >= 0 else None


def _cover_url(value: Any) -> str | None:
    return f"{COVERS_BASE_URL}/{value}-M.jpg" if isinstance(value, int) and value > 0 else None


def _source_url(key: str) -> str:
    return f"{OPEN_LIBRARY_BASE_URL}{key}"


def _description(value: Any) -> str | None:
    if isinstance(value, dict):
        return _optional_text(value.get("value"))
    return _optional_text(value)


def _detail_authors(value: Any) -> tuple[list[str], list[str]]:
    names: list[str] = []
    keys: list[str] = []
    for author in _iter_values(value):
        if not isinstance(author, dict):
            continue
        name = _optional_text(author.get("name"))
        if name and name not in names:
            names.append(name)
        reference = author.get("author") if isinstance(author.get("author"), dict) else author
        key = _optional_text(reference.get("key")) if isinstance(reference, dict) else None
        if key and re.fullmatch(r"/authors/OL\d+A", key) and key not in keys:
            keys.append(key)
    return names[:10], keys[:10]


def _work_key(value: Any) -> str | None:
    first = _first(value)
    if isinstance(first, dict):
        key = _optional_text(first.get("key"))
        if key and re.fullmatch(r"/works/OL\d+W", key):
            return key
    return None


def _first(value: Any) -> Any:
    values = _iter_values(value)
    return values[0] if values else None
