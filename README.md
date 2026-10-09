# CAPITU IA

Chatbot inteligente de descoberta bibliográfica para a atividade A3 de Inteligência Artificial. Este repositório contém a estrutura aprovada do projeto e os schemas de contrato E01; as funcionalidades do chatbot e a rota HTTP ainda estão em desenvolvimento.

## Documentação

Consulte [`docs/README.md`](docs/README.md) para os documentos de planejamento e a regra de sincronização PDF/Markdown.

## Estrutura

- `app/`: interface HTTP e schemas.
- `nlp/`: pré-processamento, similaridade TF-IDF e entidades.
- `dialogue/`: contexto, política e orquestração.
- `services/`: Open Library, normalização e cache opcional.
- `responses/` e `static/`: respostas e chat web local.
- `data/`, `artifacts/`, `evaluation/` e `tests/`: dados, avaliações e testes.
- `docs/`: requisitos, arquitetura, planejamento e evidências.

## Estado

Planejamento aprovado pelo professor conforme informado pela equipe. E01 define o contrato v1, os schemas Pydantic e seus testes unitários. A rota HTTP, PLN, integração com Open Library e avaliação funcional continuam pendentes.
