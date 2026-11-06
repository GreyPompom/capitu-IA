"""Cache TTL em memória para payloads públicos da Open Library."""

from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
from threading import RLock
from time import monotonic
from typing import Any, Callable


@dataclass(frozen=True)
class CacheStats:
    hits: int
    misses: int
    entries: int


class ResponseCache:
    """Cache pequeno, local e não persistente; falhas nunca são armazenadas."""

    def __init__(self, *, ttl_seconds: float = 60.0, clock: Callable[[], float] = monotonic) -> None:
        if ttl_seconds <= 0:
            raise ValueError("O TTL do cache deve ser positivo.")
        self.ttl_seconds = ttl_seconds
        self._clock = clock
        self._values: dict[str, tuple[float, dict[str, Any]]] = {}
        self._hits = 0
        self._misses = 0
        self._lock = RLock()

    def get(self, key: str) -> dict[str, Any] | None:
        with self._lock:
            entry = self._values.get(key)
            if entry and entry[0] > self._clock():
                self._hits += 1
                return deepcopy(entry[1])
            self._misses += 1
            if entry:
                self._values.pop(key, None)
            return None

    def set(self, key: str, payload: dict[str, Any]) -> None:
        with self._lock:
            self._values[key] = (self._clock() + self.ttl_seconds, deepcopy(payload))

    def stats(self) -> CacheStats:
        with self._lock:
            return CacheStats(hits=self._hits, misses=self._misses, entries=len(self._values))
