"""Armazenamento em memória do contexto mínimo por sessão da CAPITU."""

from __future__ import annotations

from threading import RLock
from uuid import UUID

from app.schemas import ConversationSession


class ConversationStore:
    """Guarda sessões somente durante a execução local, sem dados persistentes."""

    def __init__(self) -> None:
        self._sessions: dict[UUID, ConversationSession] = {}
        self._lock = RLock()

    def get_or_create(self, session_id: UUID) -> ConversationSession:
        with self._lock:
            session = self._sessions.setdefault(session_id, ConversationSession(session_id=session_id))
            return session.model_copy(deep=True)

    def save(self, session: ConversationSession) -> ConversationSession:
        with self._lock:
            self._sessions[session.session_id] = session.model_copy(deep=True)
            return session.model_copy(deep=True)

    def clear(self, session_id: UUID) -> ConversationSession:
        """Remove somente o contexto em memória da sessão informada."""

        with self._lock:
            session = ConversationSession(session_id=session_id)
            self._sessions[session_id] = session
            return session.model_copy(deep=True)
