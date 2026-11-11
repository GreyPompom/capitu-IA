"""Extração determinística de parâmetros bibliográficos da CAPITU.

As regras recebem a intenção já decidida pela E04/E05. Elas preservam a grafia
da entidade no texto do usuário e não consultam dataset, sessão ou API externa.
Contexto de seleção ("o segundo", "essa obra") é responsabilidade da E07.
"""

from __future__ import annotations

from dataclasses import dataclass
import re
import unicodedata

from app.schemas import EntitySlot, ExtractedEntities, Intent


QUOTED_TEXT = re.compile(r"[\"“”'](?P<entity>[^\"“”']+)[\"“”']")
ISBN_PATTERN = re.compile(r"\b(?:ISBN(?:-1[03])?\s*[:#]?\s*)?(?P<isbn>97[89][\d\s-]{10,17}|\d[\d\s-]{8,15}[\dXx])\b")

AUTHOR_PATTERNS = (
    r"\blivros\s+(?P<entity>.+?)\s+escreveu\b",
    r"\busando\s+(?P<entity>.+?)\s+como\s+autora?\b",
    r"\btitulos\s+que\s+tenham\s+(?P<entity>.+?)\s+como\s+autor\b",
    r"\bautoria\s*:\s*(?P<entity>.+?)(?:[.;?!]|$)",
    r"\bnome\s+que\s+me\s+interessa\s+e(?:h)?\s+(?P<entity>.+?)(?:\.\s+que|[;,?!]|$)",
    r"\b(?:obras|livros)\s+publicadas\s+por\s+(?P<entity>.+?)(?:[.;?!]|$)",
    r"\bobras\s+assinadas\s+por\s+(?P<entity>.+?)(?:[.;?!]|$)",
    r"\b(?:algo|coisa)\s+do\s+(?P<entity>.+?)(?:[.;?!]|$)",
    r"\b(?:alguma\s+coisa\s+)?escrita\s+por\s+(?P<entity>.+?)(?:[.;?!]|$)",
    r"\btem\s+da\s+(?P<entity>.+)$",
    r"\blivros\s+do\s+autor\s+(?P<entity>.+)$",
    r"\btem\s+da\s+(?P<entity>.+)$",
    r"\bbibliografia\s+de\s+(?P<entity>.+)$",
    r"\bescritora\s+(?P<entity>.+?)(?:[;,?.!]|$)",
    r"\bprodu[cç][aã]o\s+de\s+(?P<entity>.+?)(?:[;,?.!]|$)",
    r"\bo\s+que\s+ha\s+de\s+(?P<entity>.+?)(?:\s+no\s+acervo|[;,?.!]|$)",
    r"\bobras\s+de\s+(?P<entity>.+?)\s+posso\b",
    r"\bautoria\s+de\s+(?P<entity>.+?)(?:[;,?.!]|$)",
    r"\btitulos\s+de\s+(?P<entity>.+?)\s+para\b",
    r"\b(?:livros|obras|titulos|publicacoes|bibliografia)\s+(?:do|da|de)\s+(?P<entity>.+)$",
    r"\b(?:autor|autora|escritora)\s+(?P<entity>.+?)(?:[;,?.!]|$)",
    r"\b(?:assinados?|escritos?)\s+por\s+(?P<entity>.+?)(?:[;,?.!]|$)",
    r"\bautoria\s+(?:seja\s+)?de\s+(?P<entity>.+?)(?:[;,?.!]|$)",
    r"\b(?P<entity>.+?)\s+como\s+autor(?:a)?\b",
    r"\bnome\s+de\s+(?P<entity>.+?)(?:\s+e\s+retorne|[;,?.!]|$)",
)

SUBJECT_PATTERNS = (
    r"\bpesquisa\s+sobre\s+(?P<entity>.+?)(?:,\s+preciso|[?.!;]|$)",
    r"\buse\s+(?P<entity>.+?)\s+como\s+assunto\b",
    r"\bmeu\s+tema\s+de\s+estudo\s+e(?:h)?\s+(?P<entity>.+?)(?:[?.!;]|$)",
    r"\bconteudo\s+que\s+me\s+interessa\s+e(?:h)?\s+(?P<entity>.+?)(?:[?.!;]|$)",
    r"\bassunto\s+seja\s+(?P<entity>.+?)(?:[?.!;]|$)",
    r"\bpesquisar\s+pelo\s+tema\s*:?\s*(?P<entity>.+?)(?:[?.!;]|$)",
    r"\btrabalho\s+de\s+(?P<entity>.+?)\s+e\s+preciso\b",
    r"\bpesquisa\s+e(?:h)?\s+feita\s+por\s+(?P<entity>.+?)(?:[?.!;]|$)",
    r"\barea\s+que\s+quero\s+explorar\s+nos\s+livros\s+e(?:h)?\s+(?P<entity>.+?)(?:[?.!;]|$)",
    r"\bestudando\s+(?P<entity>.+?)\s+e\s+preciso\b",
    r"\bminha\s+pesquisa\s+eh\s+sobre\s+(?P<entity>.+?)(?:[?.!;]|$)",
    r"\bque\s+expliquem\s+(?P<entity>.+?)(?:[?.!;]|$)",
    r"\bobras\s+tratam\s+de\s+(?P<entity>.+?)(?:[?.!;]|$)",
    r"\blivros\s+que\s+abordem\s+(?P<entity>.+?)(?:[?.!;]|$)",
    r"\breferencias\s+bibliograficas\s+de\s+(?P<entity>.+?)(?:[?.!;]|$)",
    r"\bsobre\s+(?P<entity>.+?)(?:[?.!;]|$)",
    r"\b(?:livros|obras|leituras|referencias)\s+de\s+(?P<entity>.+?)(?:[?.!;]|$)",
    r"\b(?:indicacoes|material)\s+(?:de|sobre)\s+(?P<entity>.+?)(?:[?.!;]|$)",
    r"\b(?:tema|assunto)\s+(?:de\s+(?:estudo|pesquisa)\s+)?(?:e|eh|é|seja)\s+(?P<entity>.+?)(?:[?.!;]|$)",
    r"\bpesquisa\s+(?:eh|é|sobre|por)\s+(?P<entity>.+?)(?:[?.!;]|$)",
    r"\bconteudo\s+que\s+me\s+interessa\s+eh\s+(?P<entity>.+?)(?:[?.!;]|$)",
    r"\barea\s+que\s+quero\s+explorar\s+nos\s+livros\s+eh\s+(?P<entity>.+?)(?:[?.!;]|$)",
    r"\bobras\s+que\s+abordem\s+(?P<entity>.+?)(?:[?.!;]|$)",
    r"\btitulos\s+relacionados\s+a\s+(?P<entity>.+?)(?:[?.!;]|$)",
)

TITLE_PATTERNS = (
    r"\bbusca\s+pra\s+mim\s+(?P<entity>.+?)(?:[?,.!;]|$)",
    r"\bvoce\s+acha\s+(?P<entity>.+?)(?:[?,.!;]|$)",
    r"\buse\s+(?P<entity>.+?)\s+como\s+titulo\b",
    r"\bgostaria\s+de\s+encontrar\s+(?P<entity>.+?)(?:[?,.!;]|$)",
    r"\blivro\s+(?P<entity>.+?)\s+aparece\b",
    r"\bregistro\s+de\s+(?P<entity>.+?)(?:[?,.!;]|$)",
    r"\blocalizar\s+(?P<entity>.+?)\s+pelo\s+titulo\b",
    r"\bnome\s+(?P<entity>.+?)\s+no\s+catalogo\b",
    r"\b(?:encontra|procurando|procure|buscar|busque|localizar|localize|achar|ache|encontre|ca[cç]ando|pesquise|pesquisa|verifique)\s+(?:o\s+livro\s+|a\s+obra\s+|o\s+titulo\s+|pelo\s+titulo\s+|o\s+nome\s+)?(?P<entity>.+)$",
    r"\b(?:livro|obra|titulo|nome)\s+(?:chamad[oa]\s+|que\s+preciso\s+localizar\s+|que\s+anotei\s+foi\s+)?(?P<entity>.+?)(?:[?,.!;]|$)",
    r"\b(?:queria\s+ler|quero\s+achar|estou\s+tentando\s+achar|onde\s+posso\s+achar)\s+(?P<entity>.+?)(?:[?,.!;]|$)",
    r"\b(?:consta|aparece)\s+(?P<entity>.+?)(?:[?,.!;]|$)",
)

DETAIL_TITLE_PATTERNS = (
    r"\b(?:consultar\s+)?detalhes(?:\s+do\s+livro)?\s*:?\s*(?P<entity>.+?)(?:[?.!;]|$)",
    r"\b(?:quero|queria|gostaria\s+de)\s+ler\s+(?:o\s+livro\s+)?(?P<entity>.+?)(?:,\s*(?:me\s+d[ea]|mostre|quero)\s+(?:um\s+)?(?:resumo|descricao)|[?.!;]|$)",
    r"\b(?:quem\s+escreveu|quem\s+e\s+o\s+autor\s+de|autoria\s+de|autor\s+de|a\s+quem\s+e\s+atribuida\s+a\s+autoria\s+de)\s+(?P<entity>.+?)(?:[?.!;]|$)",
    r"\bisbn(?:s)?\s+constam\s+para\s+as\s+edicoes\s+de\s+(?P<entity>.+?)(?:[?.!;]|$)",
    r"\b(?:sobre|para|ficha\s+de)\s+(?P<entity>.+?)(?:,|;|\.|\?|!|$)",
    r"\b(?:resumo\s+consta\s+para|isbn(?:s)?\s+constam\s+para|editora\s+publicou)\s+(?P<entity>.+?)(?:[?.!;]|$)",
    r"\b(?:ano\s+saiu\s+a\s+primeira\s+edicao\s+de|foi\s+publicado\s+originalmente)\s+(?P<entity>.+)$",
    r"\bqual\s+escritora\s+escreveu\s+(?P<entity>.+?)(?:[?.!;]|$)",
    r"\bde\s+que\s+assunto\s+trata\s+o\s+livro\s+(?P<entity>.+?)(?:[?.!;]|$)",
    r"\bquantas\s+edicoes\s+existem\s+de\s+(?P<entity>.+?)(?:[?.!;]|$)",
    r"\bedicoes\s+de\s+(?P<entity>.+?)(?:[?.!;]|$)",
)

CONTEXT_REFERENCE_PATTERN = re.compile(r"\b(?:essa\s+obra|(?:sobre\s+)?a\s+obra|desse\s+livro|dessa\s+edicao|primeiro\s+livro|segundo\s+livro|livro\s+\d+|item\s+\d+|terceiro\s+resultado|isso|obra\s+que\s+acabei|selecionar\s+uma\s+obra)\b")

REQUESTED_FIELD_PATTERNS = (
    ("isbn", r"\bisbn(?:s)?\b"),
    ("edition_count", r"\bquantas\s+edicoes\b|\bnumero\s+de\s+edicoes\b|\bquantas\s+versoes\b"),
    ("publisher", r"\beditora\b|\bquem\s+publicou\b|\bpublicadora\b"),
    ("description", r"\bdescricao\b|\bresumo\b|\bsinopse\b|\bsobre\s+o\s+que\s+e\b"),
    ("subjects", r"\bde\s+que\s+assunto\b|\bde\s+que\s+trata\b|\bquais\s+(?:sao\s+)?os\s+assuntos\b"),
    ("first_publish_year", r"\bano\b|\bdata\b|\bquando\b|\blancad[oa]\b|\bpublicad[oa]\b|\bprimeira\s+edicao\b"),
    ("author", r"\bautor(?:ia)?\b|\bescritor(?:a)?\b|\bquem\s+escreveu\b|\bquem\s+criou\b"),
)


@dataclass(frozen=True)
class EntityExtraction:
    """Entidades e sinais necessários para a próxima decisão de diálogo."""

    entities: ExtractedEntities
    missing_required: tuple[EntitySlot, ...] = ()
    conflicts: tuple[str, ...] = ()

    @property
    def needs_clarification(self) -> bool:
        return bool(self.missing_required or self.conflicts)


def extract_entities(message: str, intent: Intent) -> EntityExtraction:
    """Extrai parâmetros para uma intenção aceita, preservando o trecho original."""

    if not isinstance(message, str) or not message.strip():
        raise ValueError("A mensagem para extração não pode estar vazia.")

    original = " ".join(message.strip().split())
    normalized, offsets = _normalize_for_matching(original)
    quotes = [_clean_entity(match.group("entity")) for match in QUOTED_TEXT.finditer(original)]
    conflicts: list[str] = []
    if len(quotes) > 1:
        conflicts.append("multiple_titles")

    title: str | None = None
    author: str | None = None
    subject: str | None = None
    isbn = _extract_isbn(original)
    requested_field: str | None = None

    if intent is Intent.SEARCH_TITLE:
        title = quotes[0] if quotes else _find_entity(original, normalized, offsets, TITLE_PATTERNS)
    elif intent is Intent.SEARCH_AUTHOR_WORKS:
        author = _find_entity(original, normalized, offsets, AUTHOR_PATTERNS)
        if _contains_composite_filter(normalized):
            conflicts.append("author_and_subject")
    elif intent is Intent.SEARCH_SUBJECT:
        subject = _find_entity(original, normalized, offsets, SUBJECT_PATTERNS)
        if subject is None:
            subject = _subject_fallback(original)
    elif intent is Intent.BOOK_DETAILS:
        if not CONTEXT_REFERENCE_PATTERN.search(normalized):
            title = quotes[0] if quotes else _find_entity(original, normalized, offsets, DETAIL_TITLE_PATTERNS)
        requested_field = _requested_field(normalized)
    else:  # pragma: no cover - proteção para expansão futura do enum
        raise ValueError(f"Intenção não suportada para extração: {intent}")

    entities = ExtractedEntities(title=title, author=author, subject=subject, isbn=isbn, requested_field=requested_field)
    return EntityExtraction(entities=entities, missing_required=_missing_required(intent, entities), conflicts=tuple(conflicts))


def _normalize_for_matching(text: str) -> tuple[str, list[int]]:
    # A normalização é interna ao matching; o valor devolvido sempre vem de
    # `original` e, portanto, mantém acentos, caixa e pontuação da pessoa usuária.
    characters: list[str] = []
    offsets: list[int] = []
    for source_index, character in enumerate(text):
        folded = "".join(
            part for part in unicodedata.normalize("NFKD", character) if not unicodedata.combining(part)
        ).casefold()
        for part in folded:
            # Mantemos delimitadores de frase para que os padrões possam parar
            # antes de explicações como "; localize os livros dela".
            characters.append(part if (part.isalnum() or part == "_" or part in ".,;?!:") else " ")
            offsets.append(source_index)

    compact_characters: list[str] = []
    compact_offsets: list[int] = []
    for character, source_index in zip(characters, offsets, strict=True):
        if character.isspace() and (not compact_characters or compact_characters[-1].isspace()):
            continue
        compact_characters.append(character)
        compact_offsets.append(source_index)
    while compact_characters and compact_characters[-1].isspace():
        compact_characters.pop()
        compact_offsets.pop()
    return "".join(compact_characters), compact_offsets


def _find_entity(original: str, normalized: str, offsets: list[int], patterns: tuple[str, ...]) -> str | None:
    for pattern in patterns:
        match = re.search(pattern, normalized, flags=re.IGNORECASE)
        if not match:
            continue
        normalized_entity = match.group("entity")
        start = offsets[match.start("entity")]
        end = offsets[match.end("entity") - 1] + 1
        candidate = _clean_entity(original[start:end])
        if candidate.casefold() in {"um livro", "uma obra", "livro", "obra", "titulo"}:
            continue
        if candidate:
            return candidate
    return None


def _clean_entity(value: str) -> str:
    value = value.strip(" \t\n\r\"“”',;:?!")
    if value.endswith(".") and not re.search(r"\b[A-Za-z]\.$", value):
        value = value[:-1]
    value = re.sub(r"\s+", " ", value)
    value = re.sub(r"\s+(?:consegue|pode|por favor|no sistema|na busca|no catalogo).*$", "", value, flags=re.IGNORECASE)
    return value.strip()


def _extract_isbn(text: str) -> str | None:
    match = ISBN_PATTERN.search(text)
    return re.sub(r"[\s-]", "", match.group("isbn")).upper() if match else None


def _requested_field(normalized: str) -> str | None:
    for field, pattern in REQUESTED_FIELD_PATTERNS:
        if re.search(pattern, normalized):
            return field
    return None


def _subject_fallback(original: str) -> str | None:
    cleaned = re.sub(r"^(?:quero|mostre|busca|procure|pesquise|tem|ha|há|preciso de|queria ler)\s+(?:livros|obras|leituras|referencias)?\s*", "", original, flags=re.IGNORECASE)
    cleaned = _clean_entity(cleaned)
    return cleaned or None


def _contains_composite_filter(normalized: str) -> bool:
    return bool(re.search(r"\b(?:livros|obras|titulos)\s+(?:de|do|da)\b.*\bsobre\b", normalized))


def _missing_required(intent: Intent, entities: ExtractedEntities) -> tuple[EntitySlot, ...]:
    if intent is Intent.SEARCH_TITLE and not entities.title:
        return (EntitySlot.TITLE,)
    if intent is Intent.SEARCH_AUTHOR_WORKS and not entities.author:
        return (EntitySlot.AUTHOR,)
    if intent is Intent.SEARCH_SUBJECT and not entities.subject:
        return (EntitySlot.SUBJECT,)
    if intent is Intent.BOOK_DETAILS and not (entities.title or entities.isbn):
        return (EntitySlot.TITLE,)
    return ()
