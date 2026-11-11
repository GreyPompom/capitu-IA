"""Composição híbrida: TF-IDF, política de segurança e regras explícitas."""

from __future__ import annotations

from dataclasses import dataclass
import re

from app.schemas import Intent, IntentDecision, IntentInterpretation
from dialogue.policy import IntentDecisionPolicy
from nlp.entity_extraction import EntityExtraction, extract_entities
from nlp.intent_similarity import IntentSimilarityIndex
from nlp.preprocessing import normalize_text


@dataclass(frozen=True)
class InterpretedMessage:
    interpretation: IntentInterpretation
    extraction: EntityExtraction | None = None


def interpret_message(
    message: str,
    index: IntentSimilarityIndex,
    policy: IntentDecisionPolicy,
) -> InterpretedMessage:
    """Interpreta uma mensagem sem chamar fonte externa ou manter contexto."""

    candidates = index.rank(message)
    policy_result = policy.interpret(message, candidates)
    if policy_result.decision is IntentDecision.OUT_OF_SCOPE:
        return InterpretedMessage(policy_result)

    rule_intent = _high_precision_intent(normalize_text(message))
    if rule_intent is not None:
        extraction = extract_entities(message, rule_intent)
        top = next((candidate for candidate in candidates if candidate.intent is rule_intent), None)
        return InterpretedMessage(
            IntentInterpretation(
                decision=IntentDecision.ACCEPTED,
                intent=rule_intent,
                similarity_score=top.similarity_score if top else None,
                # A regra, não a diferença entre candidatos, autorizou a decisão.
                # Portanto, margem não é aplicável neste caminho híbrido.
                margin=None,
                candidates=candidates,
                entities=extraction.entities,
            ),
            extraction,
        )

    if policy_result.decision is IntentDecision.ACCEPTED and policy_result.intent is not None:
        extraction = extract_entities(message, policy_result.intent)
        return InterpretedMessage(
            policy_result.model_copy(update={"entities": extraction.entities}),
            extraction,
        )
    return InterpretedMessage(policy_result)


def _high_precision_intent(normalized: str) -> Intent | None:
    """Reconhece comandos inequívocos; casos genéricos continuam no TF-IDF."""

    if re.search(r"\b(?:quem\s+escreveu|quem\s+e\s+o\s+autor|qual\s+(?:e\s+)?(?:o\s+)?autor|isbn|editora|descricao|resumo|detalhes|quantas\s+edicoes|de\s+que\s+ano|todas?\s+as\s+informacoes|todos?\s+os\s+dados|tudo\s+sobre)\b", normalized):
        return Intent.BOOK_DETAILS
    if re.search(r"\b(?:liste|listar|mostre|mostrar)\s+(?:as\s+)?(?:obras|livros|titulos|publicacoes)\s+(?:de|do|da)\b", normalized):
        return Intent.SEARCH_AUTHOR_WORKS
    if re.search(r"\b(?:livros|obras|titulos|publicacoes)\b.*\b(?:escreveu|assinad|autoria)\b", normalized):
        return Intent.SEARCH_AUTHOR_WORKS
    if re.search(r"\b(?:livros|obras|leituras)\s+sobre\b|\b(?:assunto|tema)\b|\bficcao\s+cientifica\b", normalized):
        return Intent.SEARCH_SUBJECT
    if re.search(r"\b(?:procure|procurar|buscar|busque|localize|localizar|encontre|encontrar|ache|achar)\b", normalized):
        return Intent.SEARCH_TITLE
    return None
