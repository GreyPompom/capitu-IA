# Validação da Interface — Integração com Backend

## Objetivo

Validar os quatro fluxos da interface previstos na task de integração com o backend, verificando as requisições enviadas e as respostas apresentadas.

## Ambiente de teste

- Aplicação local: `http://127.0.0.1:8000`
- Endpoint: `POST /api/chat`
- Navegador: Opera
- API: ambiente local

## UI-05 — Busca por título

**Consulta realizada:** `Procure Dom Casmurro`

**Resultado:** Requisição enviada com sucesso (HTTP 200). A API reconheceu a intenção buscar_por_titulo, retornou cinco referências de livros com state: awaiting_selection, e a interface apresentou a lista de resultados.

**Status:** Comunicação e renderização validadas.

## UI-06 — Busca por autor

**Consulta realizada**: Obras do autor: Machado de Assis

**Resultado**: Requisição enviada com sucesso (HTTP 200). A API reconheceu a `intenção buscar_obras_autor`, mas retornou `state: no_results` e uma lista vazia.

**Resultado Visual:** A interface apresentou corretamente a mensagem recebida: `"Não encontrei referências na Open Library para essa busca`. Isso não comprova que a obra não exista."

**Observação**: O teste inicial com o atalho incompleto `Obras do autor:` também foi realizado. A API retornou `awaiting_clarification`, pois não havia nome de autor informado.

**Status:** Comunicação e renderização validadas. Consulta sem resultados na fonte externa.

## UI-07 — Busca por assunto

**Consulta realizada**: Quero livros sobre ficção científica

**Resultado:** Requisição enviada com sucesso (HTTP 200). A API reconheceu a intenção `buscar_por_assunto`, retornou `state: awaiting_selection` e cinco referências de livros.

**Resultado visual**: A interface apresentou a mensagem de seleção e os resultados recebidos.

**Status:** Comunicação e renderização validadas com resultados.

## UI-08 — Consulta de detalhes

### Teste 1 — Clique no cartão

**Ação**: Clique no cartão de Dom Casmurro.

**Payload:** `Consultar detalhes do livro: Dom Casmurro`

**Resultado:** A API reconheceu `consultar_detalhes`, mas retornou `awaiting_clarification`, solicitando o título da obra.

### Teste 2 — Pergunta sobre autoria

**Payload:** `Quem escreveu Dom Casmurro?`

**Resultado:** A API reconheceu `consultar_detalhes`, retornou `awaiting_selection` e apresentou cinco resultados.

### Teste 3 — Consulta direta

**Payload:** `Detalhes de Dom Casmurro`

**Resultado:** A API reconheceu `consultar_detalhes`, mas retornou `awaiting_clarification`, solicitando novamente o título da obra.

### Teste 4 — Seleção de livro por assunto

**Ação:** Clique no cartão de Ape and Essence, após a busca por ficção científica.

**Payload:** `Consultar detalhes do livro: Ape and essence`

**Resultado:** A API retornou `awaiting_clarification`, solicitando o título da obra.

### Teste 5 — Consulta direta do livro selecionado

**Payload:** `Detalhes de Ape and Essence`

**Resultado:** A API retornou novamente `awaiting_clarification`, solicitando o título da obra.

**Observação:** Nos testes de detalhes, a interface enviou as mensagens e apresentou as respostas recebidas. Entretanto, a continuidade da consulta não ocorreu conforme o fluxo esperado. Divergência pendente de investigação no backend.

**Status:** Envio e renderização validados. Fluxo completo de consulta de detalhes pendente.

## Evidências

- `docs/evidence/UI-07-resultados-parte-1.png`
- `docs/evidence/UI-07-resultados-parte-2.png`