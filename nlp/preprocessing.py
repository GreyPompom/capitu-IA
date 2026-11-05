"""Normalização textual determinística usada pelo índice de intenções."""

from __future__ import annotations

import re
import unicodedata


_WHITESPACE = re.compile(r"\s+")
_NON_WORD = re.compile(r"[^\w\s]")


def normalize_text(text: str) -> str:
    """Normaliza texto sem remover palavras que possam distinguir intenções.

    O texto original é preservado no dataset e nas entidades. Esta função prepara
    somente a representação TF-IDF: unifica Unicode, remove acentos e pontuação,
    reduz para minúsculas e normaliza espaços. Não remove stopwords, pois termos
    como "de", "por" e "sobre" podem ajudar a diferenciar formulações curtas.
    """

    if not isinstance(text, str):
        raise TypeError("A mensagem para normalização deve ser uma string.")

    decomposed = unicodedata.normalize("NFKD", text)
    without_accents = "".join(
        character for character in decomposed if not unicodedata.combining(character)
    )
    without_punctuation = _NON_WORD.sub(" ", without_accents.casefold())
    return _WHITESPACE.sub(" ", without_punctuation).strip()
