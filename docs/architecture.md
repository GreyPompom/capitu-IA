# Arquitetura

A decisão técnica detalhada e o fluxo estão no [planejamento detalhado da equipe](CAPITU_Planejamento_Detalhado_Equipe.md). Esta página serve como índice e deve ser atualizada junto ao planejamento se os componentes ou limites mudarem. O contrato HTTP versionado da E01 está em [`contracts/chat-v1.md`](contracts/chat-v1.md); seu status é proposta pronta para revisão por Millena e Miguel.

## Fluxo planejado

Usuário → chat web local → backend FastAPI → pré-processamento → interpretação de intenção (TF-IDF/similaridade) → extração de entidades → política e contexto mínimo → cliente Open Library → normalização → resposta.

## Tecnologias acordadas

- Python e FastAPI para o backend local.
- scikit-learn para representação TF-IDF e cálculo de similaridade.
- httpx para chamadas HTTP à Open Library.
- HTML, CSS e JavaScript para a interface web simples.

## Limites

A CAPITU ajuda na descoberta bibliográfica usando dados públicos. Não representa o acervo da universidade e não opera empréstimos, renovações, reservas, compras nem recomendações personalizadas. Os resultados dependem da cobertura e disponibilidade da Open Library.

## Contrato executável da E01

[`app/schemas.py`](../app/schemas.py) define os modelos Pydantic v2 para mensagens, pedidos, interpretação, entidades, livros, resposta e contexto de sessão. A E02 conectará o endpoint `POST /api/chat` ao orquestrador e adicionará testes HTTP com resposta simulada, sem chamar a API externa.
