"""Política determinística de aceitação, ambiguidade e abstinência da CAPITU.

Esta camada recebe candidatos produzidos pelo TF-IDF.  Ela não calcula a
similaridade, não extrai entidades e não consulta a Open Library: somente
decide se há evidência suficiente para o próximo passo do diálogo.
"""

from __future__ import annotations

from dataclasses import dataclass
import re
from typing import Sequence

from app.schemas import (
    ExtractedEntities,
    IntentCandidate,
    IntentDecision,
    IntentInterpretation,
)
from nlp.preprocessing import normalize_text


# Regras de exclusão operacional previstas no escopo aprovado. Elas são
# verificadas antes do score para que citar um livro não transforme uma reserva,
# empréstimo ou multa em consulta bibliográfica.
OUT_OF_SCOPE_PATTERNS = (
    r"\bemprest", r"\brenov", r"\breserv", r"\bmulta\b", r"\bacervo\b",
    r"\bestante\b", r"\bcompr", r"\bpag", r"\bprevisao do tempo\b",
    r"\bcapital do brasil\b", r"\bquanto e\b", r"\btraduza\b",
    r"\bhistorico de leitura\b", r"\bbiografia completa\b",
    r"\bcapitulo por capitulo\b",
)

# Formulações que não descrevem uma ação bibliográfica única sem contexto.
AMBIGUOUS_PATTERNS = (
    r"^me fala sobre\b", r"\bprimeiro\b", r"\bsegundo\b", r"\bterceiro\b",
    r"\bdele\b", r"\bdela\b", r"^o livro do autor de\b",
)
AMBIGUOUS_SINGLE_TERMS = {"romance"}


@dataclass(frozen=True)
class IntentPolicyConfig:
    """Parâmetros congelados após análise do conjunto de validação da E05.

    Os valores são limiares de similaridade cosseno e não probabilidades.
    """

    acceptance_threshold: float = 0.25
    ambiguity_margin: float = 0.12

    def __post_init__(self) -> None:
        for name, value in (
            ("acceptance_threshold", self.acceptance_threshold),
            ("ambiguity_margin", self.ambiguity_margin),
        ):
            if not 0.0 <= value <= 1.0:
                raise ValueError(f"{name} deve estar entre 0 e 1.")


class IntentDecisionPolicy:
    """Aplica precedência de escopo, evidência, limiar e margem."""

    def __init__(self, config: IntentPolicyConfig | None = None) -> None:
        self.config = config or IntentPolicyConfig()

    def interpret(
        self,
        message: str,
        candidates: Sequence[IntentCandidate],
        *,
        entities: ExtractedEntities | None = None,
    ) -> IntentInterpretation:
        """Transforma ranking em decisão, sem assumir que score é probabilidade."""

        normalized = normalize_text(message)
        ordered = _ordered_candidates(candidates)
        top = ordered[0] if ordered else None
        second = ordered[1] if len(ordered) > 1 else None
        score = top.similarity_score if top else None
        margin = (top.similarity_score - second.similarity_score) if second else None
        common = {
            "similarity_score": score,
            "margin": margin,
            "candidates": ordered,
            "entities": entities or ExtractedEntities(),
        }

        if _matches_any(normalized, OUT_OF_SCOPE_PATTERNS):
            return IntentInterpretation(decision=IntentDecision.OUT_OF_SCOPE, **common)

        if _is_known_ambiguity(normalized, score):
            return IntentInterpretation(decision=IntentDecision.AMBIGUOUS, **common)

        if top is None or top.similarity_score == 0.0:
            return IntentInterpretation(decision=IntentDecision.REJECTED, **common)

        if top.similarity_score < self.config.acceptance_threshold:
            return IntentInterpretation(decision=IntentDecision.REJECTED, **common)

        if margin is not None and margin < self.config.ambiguity_margin:
            return IntentInterpretation(decision=IntentDecision.AMBIGUOUS, **common)

        return IntentInterpretation(
            decision=IntentDecision.ACCEPTED,
            intent=top.intent,
            **common,
        )


def _ordered_candidates(candidates: Sequence[IntentCandidate]) -> list[IntentCandidate]:
    """Valida e ordena candidatos para tornar a política independente do chamador."""

    if len(candidates) > 3:
        raise ValueError("A política aceita no máximo três candidatos.")
    ranks = [candidate.rank for candidate in candidates]
    if len(set(ranks)) != len(ranks):
        raise ValueError("Os candidatos precisam ter ranks distintos.")
    return sorted(candidates, key=lambda candidate: candidate.rank)


def _matches_any(message: str, patterns: Sequence[str]) -> bool:
    return any(re.search(pattern, message) for pattern in patterns)


def _is_known_ambiguity(message: str, score: float | None) -> bool:
    if _matches_any(message, AMBIGUOUS_PATTERNS):
        return True
    if message in AMBIGUOUS_SINGLE_TERMS or message.isdigit():
        return True

    # Uma referência nominal curta, com alguma evidência no corpus, não informa
    # se o usuário quer título, autor, assunto ou detalhes. Texto sem evidência
    # continua rejeitado (não é promovido a ambíguo).
    words = message.split()
    return bool(score and 0.0 < score and len(words) <= 4 and not _has_action_word(words))


def _has_action_word(words: Sequence[str]) -> bool:
    action_stems = ("procure", "buscar", "busque", "mostre", "liste", "quero", "quem", "qual", "tem")
    return any(word.startswith(action_stems) for word in words)
