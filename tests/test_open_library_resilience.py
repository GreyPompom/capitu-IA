"""Testes E10: falhas transitórias, ritmo e cache sem chamadas externas."""

import json
from datetime import datetime, timezone
from pathlib import Path

import httpx
import pytest

from services.cache import ResponseCache
from services.open_library import OpenLibraryClient, OpenLibraryUnavailableError, RequestPacer, _retry_delay


FIXTURES = Path(__file__).parent / "fixtures"


def payload(name: str) -> dict:
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


def client_with(handler, *, sleeps=None, cache=None, pacer=None, max_retries=1) -> OpenLibraryClient:
    transport = httpx.MockTransport(handler)
    return OpenLibraryClient(
        httpx.Client(transport=transport, base_url="https://openlibrary.org"),
        pacer=pacer or RequestPacer(minimum_interval_seconds=0),
        sleeper=(sleeps.append if sleeps is not None else lambda _: None),
        cache=cache,
        max_retries=max_retries,
    )


def test_timeout_retries_once_then_returns_controlled_result() -> None:
    calls = 0
    sleeps: list[float] = []

    def handler(request: httpx.Request) -> httpx.Response:
        nonlocal calls
        calls += 1
        if calls == 1:
            raise httpx.ReadTimeout("timeout", request=request)
        return httpx.Response(200, json=payload("search_single.json"), request=request)

    books = client_with(handler, sleeps=sleeps).search_by_title("Quarto de Despejo")

    assert calls == 2
    assert sleeps == [0.25]
    assert books[0].title == "Quarto de Despejo"


def test_429_respects_retry_after_before_single_retry() -> None:
    calls = 0
    sleeps: list[float] = []

    def handler(request: httpx.Request) -> httpx.Response:
        nonlocal calls
        calls += 1
        if calls == 1:
            return httpx.Response(429, headers={"Retry-After": "2"}, request=request)
        return httpx.Response(200, json=payload("search_single.json"), request=request)

    books = client_with(handler, sleeps=sleeps).search_by_title("Quarto de Despejo")

    assert calls == 2
    assert sleeps == [2.0]
    assert books


def test_503_stops_after_one_retry_without_loop() -> None:
    calls = 0
    sleeps: list[float] = []

    def handler(request: httpx.Request) -> httpx.Response:
        nonlocal calls
        calls += 1
        return httpx.Response(503, request=request)

    with pytest.raises(OpenLibraryUnavailableError):
        client_with(handler, sleeps=sleeps).search_by_title("Duna")

    assert calls == 2
    assert sleeps == [0.25]


def test_invalid_json_is_not_retried() -> None:
    calls = 0

    def handler(request: httpx.Request) -> httpx.Response:
        nonlocal calls
        calls += 1
        return httpx.Response(200, content=b"not-json", request=request)

    with pytest.raises(OpenLibraryUnavailableError):
        client_with(handler).search_by_title("Duna")

    assert calls == 1


def test_empty_result_is_valid_and_cached() -> None:
    calls = 0
    cache = ResponseCache(ttl_seconds=60)

    def handler(request: httpx.Request) -> httpx.Response:
        nonlocal calls
        calls += 1
        return httpx.Response(200, json=payload("search_empty.json"), request=request)

    client = client_with(handler, cache=cache)
    assert client.search_by_title("Inexistente") == []
    assert client.search_by_title("Inexistente") == []
    assert calls == 1
    assert cache.stats().hits == 1


def test_pacer_reserves_interval_across_sessions() -> None:
    now = [0.0]
    sleeps: list[float] = []

    def clock() -> float:
        return now[0]

    def sleeper(delay: float) -> None:
        sleeps.append(delay)
        now[0] += delay

    pacer = RequestPacer(minimum_interval_seconds=1.0, clock=clock, sleeper=sleeper)
    pacer.wait()
    pacer.wait()
    pacer.wait()

    assert sleeps == [1.0, 1.0]


def test_retry_after_http_date_is_converted_to_delay() -> None:
    now = datetime(2026, 11, 5, 12, 0, tzinfo=timezone.utc)

    delay = _retry_delay("Wed, 05 Nov 2026 12:00:03 GMT", lambda: now)

    assert delay == 3.0
