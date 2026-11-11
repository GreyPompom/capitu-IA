"""Textos determinísticos para resultados bibliográficos da CAPITU."""

from __future__ import annotations

from app.schemas import BookDetails, BookSummary, ConversationState, ExtractedEntities, Intent


def search_text(intent: Intent, entities: ExtractedEntities, results: list[BookSummary], state: ConversationState) -> str:
    """Gera texto para busca sem alegar completude ou acervo local."""

    if state is ConversationState.NO_RESULTS:
        return "Não encontrei referências na Open Library para essa busca. Isso não comprova que a obra não exista."
    if state is ConversationState.AWAITING_SELECTION:
        return f"Encontrei {len(results)} referências na Open Library. Escolha uma posição, por exemplo: ‘o segundo’."

    subject = {
        Intent.SEARCH_TITLE: entities.title,
        Intent.SEARCH_AUTHOR_WORKS: entities.author,
        Intent.SEARCH_SUBJECT: entities.subject,
    }.get(intent)
    label = {
        Intent.SEARCH_TITLE: "título",
        Intent.SEARCH_AUTHOR_WORKS: "autor",
        Intent.SEARCH_SUBJECT: "assunto",
    }.get(intent, "consulta")
    return f"Encontrei {len(results)} referência(s) para {label} ‘{subject or 'informado'}’ na Open Library."


def detail_text(details: BookDetails, requested_field: str | None) -> str:
    """Mostra somente o campo pedido que a fonte realmente forneceu."""

    values = {
        "author": _joined(details.authors),
        "first_publish_year": str(details.first_publish_year) if details.first_publish_year is not None else None,
        "isbn": _joined(details.isbn),
        "publisher": _joined(details.publishers),
        "description": details.description,
        "subjects": _joined(details.subjects),
        "edition_count": str(details.edition_count) if details.edition_count is not None else None,
    }
    if requested_field:
        value = values.get(requested_field)
        if value:
            labels = {
                "author": "Autoria",
                "first_publish_year": "Primeira publicação",
                "isbn": "ISBN",
                "publisher": "Editora",
                "description": "Descrição",
                "subjects": "Assuntos",
                "edition_count": "Edições",
            }
            return f"{labels.get(requested_field, 'Informação')} de ‘{details.title}’: {value}. Fonte: Open Library."
        if requested_field == "first_publish_year" and details.publication_date:
            return (
                f"A Open Library não forneceu a primeira publicação de ‘{details.title}’, "
                f"mas informa a data de publicação disponível: {details.publication_date}. Fonte: Open Library."
            )
        return f"A Open Library não forneceu esse campo para ‘{details.title}’. Fonte: Open Library."

    summary = [f"Título: {details.title}"]
    if details.authors:
        summary.append(f"Autoria: {_joined(details.authors)}")
    if details.first_publish_year is not None:
        summary.append(f"Primeira publicação: {details.first_publish_year}")
    if details.description:
        summary.append(f"Descrição: {details.description}")
    return ". ".join(summary) + ". Fonte: Open Library."


def source_unavailable_text() -> str:
    return "A Open Library está indisponível no momento. Tente novamente mais tarde."


def _joined(values: list[str]) -> str | None:
    return ", ".join(values) if values else None
