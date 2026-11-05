"""Máquina de estados para pendências, resultados e seleção por sessão."""

from __future__ import annotations

from dataclasses import dataclass, field
import re
from uuid import UUID

from app.schemas import (
    BookSummary,
    ConversationSession,
    ConversationState,
    EntitySlot,
    ExtractedEntities,
    Intent,
    IntentDecision,
    IntentInterpretation,
)
from dialogue.context import ConversationStore
from nlp.entity_extraction import EntityExtraction
from nlp.preprocessing import normalize_text


CANCEL_PATTERN = re.compile(r"^(?:cancelar|cancele|cancela|desistir|esquecer|parar|sair)\b")
ORDINAL_SELECTIONS = {
    "primeiro": 1,
    "primeira": 1,
    "segundo": 2,
    "segunda": 2,
    "terceiro": 3,
    "terceira": 3,
    "quarto": 4,
    "quarta": 4,
    "quinto": 5,
    "quinta": 5,
}


@dataclass(frozen=True)
class DialogueOutcome:
    """Resultado interno que a integração posterior converterá em resposta HTTP."""

    session: ConversationSession
    text: str
    intent: Intent | None = None
    entities: ExtractedEntities = field(default_factory=ExtractedEntities)
    should_query: bool = False
    selected_book: BookSummary | None = None


class DialogueManager:
    """Controla estado curto sem classificar mensagens nem consultar fontes."""

    def __init__(self, store: ConversationStore | None = None) -> None:
        self.store = store or ConversationStore()

    def handle_interpretation(
        self,
        session_id: UUID,
        message: str,
        interpretation: IntentInterpretation,
        extraction: EntityExtraction | None = None,
    ) -> DialogueOutcome:
        """Aplica precedência de cancelamento, nova demanda, pendência e seleção."""

        session = self.store.get_or_create(session_id)
        normalized = normalize_text(message)

        if CANCEL_PATTERN.search(normalized):
            return self._save_outcome(
                ConversationSession(session_id=session_id),
                "Certo, cancelei a solicitação anterior. Como posso ajudar com livros?",
            )

        # Uma intenção aceita representa uma nova demanda explícita e sempre
        # substitui contexto anterior, conforme o contrato E01.
        if interpretation.decision is IntentDecision.ACCEPTED:
            return self._handle_accepted(session, interpretation, extraction)

        selection = _selection_number(normalized)
        if selection is not None and session.last_results:
            return self._handle_selection(session, selection)

        if session.pending_intent and session.pending_parameter:
            return self._handle_pending_answer(session, message)

        if interpretation.decision is IntentDecision.OUT_OF_SCOPE:
            session = session.model_copy(
                update={"state": ConversationState.OUT_OF_SCOPE, "pending_intent": None, "pending_parameter": None}
            )
            return self._save_outcome(session, "Posso ajudar com buscas e dados bibliográficos, mas essa solicitação está fora do escopo.")

        session = session.model_copy(
            update={"state": ConversationState.AWAITING_CLARIFICATION, "pending_intent": None, "pending_parameter": None}
        )
        return self._save_outcome(session, "Não identifiquei com segurança a busca. Informe o título, autor ou assunto que deseja consultar.")

    def record_search_results(
        self,
        session_id: UUID,
        intent: Intent,
        entities: ExtractedEntities,
        results: list[BookSummary],
    ) -> DialogueOutcome:
        """Registra até cinco resultados normalizados após a consulta futura à fonte."""

        if len(results) > 5:
            raise ValueError("A sessão aceita no máximo cinco resultados por turno.")
        session = self.store.get_or_create(session_id)
        session = session.model_copy(update={"pending_intent": None, "pending_parameter": None, "last_results": results})
        if not results:
            session = session.model_copy(update={"state": ConversationState.NO_RESULTS, "selected_book": None})
            return self._save_outcome(session, "Não encontrei resultados para essa busca.", intent=intent, entities=entities)
        if len(results) == 1:
            session = session.model_copy(update={"state": ConversationState.ANSWERED, "selected_book": results[0]})
            return self._save_outcome(session, "Encontrei uma obra. Você pode pedir detalhes sobre ela.", intent=intent, entities=entities, selected_book=results[0])

        session = session.model_copy(update={"state": ConversationState.AWAITING_SELECTION, "selected_book": None})
        return self._save_outcome(
            session,
            f"Encontrei {len(results)} obras. Escolha uma posição, por exemplo: ‘o segundo’. ",
            intent=intent,
            entities=entities,
        )

    def _handle_accepted(
        self,
        session: ConversationSession,
        interpretation: IntentInterpretation,
        extraction: EntityExtraction | None,
    ) -> DialogueOutcome:
        assert interpretation.intent is not None
        entities = extraction.entities if extraction else interpretation.entities
        missing = extraction.missing_required if extraction else ()
        conflicts = extraction.conflicts if extraction else ()

        # Um pedido de detalhes sem obra explícita pode usar apenas a seleção da
        # mesma sessão; não reaproveita resultados de outras sessões.
        if (
            interpretation.intent is Intent.BOOK_DETAILS
            and missing
            and session.selected_book is not None
            and not conflicts
        ):
            entities = entities.model_copy(update={"title": session.selected_book.title})
            clean = _clear_transient_context(session)
            return self._save_outcome(
                clean,
                "Vou consultar os detalhes da obra selecionada.",
                intent=interpretation.intent,
                entities=entities,
                should_query=True,
                selected_book=session.selected_book,
            )

        clean = _clear_transient_context(session)
        if conflicts:
            session = clean.model_copy(update={"state": ConversationState.AWAITING_CLARIFICATION})
            return self._save_outcome(session, "Encontrei informações que pedem confirmação. Informe uma busca por vez.")
        if missing:
            parameter = missing[0]
            session = clean.model_copy(
                update={
                    "state": ConversationState.AWAITING_CLARIFICATION,
                    "pending_intent": interpretation.intent,
                    "pending_parameter": parameter,
                }
            )
            return self._save_outcome(session, _missing_prompt(parameter), intent=interpretation.intent, entities=entities)

        return self._save_outcome(
            clean,
            "Entendi a busca. A consulta bibliográfica pode ser realizada.",
            intent=interpretation.intent,
            entities=entities,
            should_query=True,
        )

    def _handle_pending_answer(self, session: ConversationSession, message: str) -> DialogueOutcome:
        assert session.pending_intent is not None and session.pending_parameter is not None
        value = _clean_fragment(message)
        if not value:
            return self._save_outcome(session, _missing_prompt(session.pending_parameter), intent=session.pending_intent)

        entities = ExtractedEntities().model_copy(update={session.pending_parameter.value: value})
        resolved_intent = session.pending_intent
        session = _clear_transient_context(session)
        return self._save_outcome(
            session,
            "Informação recebida. A consulta bibliográfica pode ser realizada.",
            intent=resolved_intent,
            entities=entities,
            should_query=True,
        )

    def _handle_selection(self, session: ConversationSession, selection: int) -> DialogueOutcome:
        if not 1 <= selection <= len(session.last_results):
            session = session.model_copy(update={"state": ConversationState.AWAITING_SELECTION})
            return self._save_outcome(
                session,
                f"Escolha uma posição entre 1 e {len(session.last_results)}.",
            )

        selected = session.last_results[selection - 1]
        session = session.model_copy(update={"state": ConversationState.ANSWERED, "selected_book": selected})
        return self._save_outcome(
            session,
            f"Você selecionou ‘{selected.title}’. O que deseja saber sobre esta obra?",
            selected_book=selected,
        )

    def _save_outcome(
        self,
        session: ConversationSession,
        text: str,
        *,
        intent: Intent | None = None,
        entities: ExtractedEntities | None = None,
        should_query: bool = False,
        selected_book: BookSummary | None = None,
    ) -> DialogueOutcome:
        return DialogueOutcome(
            session=self.store.save(session),
            text=text,
            intent=intent,
            entities=entities or ExtractedEntities(),
            should_query=should_query,
            selected_book=selected_book,
        )


def _clear_transient_context(session: ConversationSession) -> ConversationSession:
    return session.model_copy(
        update={
            "state": ConversationState.IDLE,
            "pending_intent": None,
            "pending_parameter": None,
            "last_results": [],
            "selected_book": None,
        }
    )


def _selection_number(normalized: str) -> int | None:
    if normalized.isdigit():
        return int(normalized)
    for word, position in ORDINAL_SELECTIONS.items():
        if re.search(rf"\b{word}\b", normalized):
            return position
    return None


def _clean_fragment(message: str) -> str:
    return " ".join(message.strip().strip("\"“”'.,;:?!").split())


def _missing_prompt(parameter: EntitySlot) -> str:
    prompts = {
        EntitySlot.TITLE: "Qual é o título da obra que você quer consultar?",
        EntitySlot.AUTHOR: "Qual é o nome do autor cujas obras você quer buscar?",
        EntitySlot.SUBJECT: "Sobre qual assunto ou gênero você quer buscar livros?",
    }
    return prompts[parameter]
