"""Schemas versionados para o contrato local do chat CAPITU v1.

O endpoint HTTP será conectado ao orquestrador na E02. Este módulo define os
modelos públicos e internos sem acoplar a interpretação à Open Library.
"""

from enum import Enum
from typing import Literal
from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict, Field, HttpUrl, field_validator, model_validator


class ContractModel(BaseModel):
    """Base stricta para detectar incompatibilidades de contrato cedo."""

    model_config = ConfigDict(extra="forbid")


class Intent(str, Enum):
    """Intenções bibliográficas aceitas no MVP."""

    SEARCH_TITLE = "buscar_por_titulo"
    SEARCH_AUTHOR_WORKS = "buscar_obras_autor"
    SEARCH_SUBJECT = "buscar_por_assunto"
    BOOK_DETAILS = "consultar_detalhes"


class IntentDecision(str, Enum):
    ACCEPTED = "accepted"
    AMBIGUOUS = "ambiguous"
    REJECTED = "rejected"
    OUT_OF_SCOPE = "out_of_scope"


class ConversationState(str, Enum):
    IDLE = "idle"
    ANSWERED = "answered"
    AWAITING_CLARIFICATION = "awaiting_clarification"
    AWAITING_SELECTION = "awaiting_selection"
    NO_RESULTS = "no_results"
    OUT_OF_SCOPE = "out_of_scope"
    SOURCE_UNAVAILABLE = "source_unavailable"


class EntitySlot(str, Enum):
    TITLE = "title"
    AUTHOR = "author"
    SUBJECT = "subject"


class ChatMessage(ContractModel):
    """Mensagem interna; não representa histórico persistido."""

    role: Literal["user", "assistant"]
    content: str = Field(min_length=1, max_length=2_000)


class ChatRequest(ContractModel):
    """Corpo aceito por POST /api/chat."""

    message: str = Field(
        min_length=1,
        max_length=1_000,
        description="Mensagem em português, entre 1 e 1000 caracteres.",
    )
    session_id: UUID | None = Field(
        default=None,
        description="Omitido no primeiro turno; reutilizado nos turnos seguintes.",
    )

    @field_validator("message")
    @classmethod
    def strip_and_reject_blank(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("A mensagem não pode conter apenas espaços.")
        return value


class ExtractedEntities(ContractModel):
    title: str | None = Field(default=None, max_length=300)
    author: str | None = Field(default=None, max_length=200)
    subject: str | None = Field(default=None, max_length=120)
    isbn: str | None = Field(default=None, max_length=20)
    year: int | None = Field(default=None, ge=0, le=9_999)
    requested_field: str | None = Field(default=None, max_length=80)


class IntentCandidate(ContractModel):
    intent: Intent
    rank: int = Field(ge=1, le=3)
    similarity_score: float = Field(
        ge=0.0,
        le=1.0,
        description="Similaridade cosseno, não probabilidade calibrada.",
    )


class IntentInterpretation(ContractModel):
    """Saída interna do interpretador antes da política de diálogo/API."""

    decision: IntentDecision
    intent: Intent | None = None
    similarity_score: float | None = Field(default=None, ge=0.0, le=1.0)
    margin: float | None = Field(default=None, ge=0.0, le=1.0)
    candidates: list[IntentCandidate] = Field(default_factory=list, max_length=3)
    entities: ExtractedEntities = Field(default_factory=ExtractedEntities)

    @model_validator(mode="after")
    def accepted_decision_has_one_intent(self) -> "IntentInterpretation":
        if (self.decision is IntentDecision.ACCEPTED) != (self.intent is not None):
            raise ValueError("Somente uma interpretação aceita deve definir uma intenção escolhida.")
        return self


class BookSummary(ContractModel):
    """Obra normalizada; campos ausentes na fonte permanecem nulos/vazios."""

    openlibrary_key: str = Field(min_length=1, max_length=120, description="Chave de obra/edição da Open Library.")
    title: str = Field(min_length=1, max_length=500)
    authors: list[str] = Field(default_factory=list, max_length=10)
    first_publish_year: int | None = Field(default=None, ge=0, le=9_999)
    edition_count: int | None = Field(default=None, ge=0)
    isbn: list[str] = Field(default_factory=list, max_length=5)
    subjects: list[str] = Field(default_factory=list, max_length=10)
    cover_url: HttpUrl | None = None
    source_url: HttpUrl


class ChatResponse(ContractModel):
    """Envelope estável para toda resposta de negócio do chat."""

    session_id: UUID
    text: str = Field(min_length=1, max_length=2_000)
    state: ConversationState
    intent: Intent | None = None
    results: list[BookSummary] = Field(default_factory=list, max_length=5)


class ConversationSession(ContractModel):
    """Contexto mínimo; não conserva transcript completo nem dados pessoais."""

    session_id: UUID = Field(default_factory=uuid4)
    state: ConversationState = ConversationState.IDLE
    pending_intent: Intent | None = None
    pending_parameter: EntitySlot | None = None
    last_results: list[BookSummary] = Field(default_factory=list, max_length=5)
