# ADR 001 Contrato HTTP do chat

- **Status:** proposta pronta para revisão da equipe.
- **Data:** 08/10/2026.
- **Responsável:** Emely.
- **Task:** E01.

## Contexto

A UI precisa integrar-se ao backend antes de a API bibliográfica real e a lógica de PLN estarem concluídas. Um contrato estável permite que a UI e os testes usem dados simulados sem atribuir inteligência à Open Library nem criar resposta enganosa.

## Decisão proposta

- `POST /api/chat` recebe `message` e `session_id` opcional.
- A resposta de negócio tem sempre `session_id`, `text`, `state`, `intent` opcional e `results` (lista).
- Quatro intenções de negócio: título, obras por autor, assunto e detalhes. Fora de escopo é decisão de política, não classe de negócio.
- A validação de entrada retorna HTTP 422; os estados de diálogo/fonte descrevem resultados válidos de negócio.
- Contexto mínimo usa UUID por sessão e guarda somente pendência e até cinco resultados; não guarda transcript completo.
- Limites 1000 caracteres por entrada, 2000 por resposta e cinco livros são valores internos provisórios para revisão.
- Interpretador e serviço externo são módulos separados; score de similaridade não é exposto à UI como probabilidade.

## Consequências

- A UI pode renderizar lista de livros mesmo quando ela está vazia e tratar estados enumerados.
- O serviço externo pode ser substituído por fixture sem alterar o contrato.
- Mudanças no estado ficam no servidor; o cliente envia somente `session_id`.
- Millena e Miguel precisam revisar compatibilidade e exemplos antes do aceite final E01.
- A E02 ainda precisa implementar a rota HTTP e automatizar cenários de request/response.

## Referências

- [Contrato v1](../contracts/chat-v1.md)
- [Planejamento aprovado](../CAPITU_Planejamento_Detalhado_Equipe.md)
- [FastAPI request body](https://fastapi.tiangolo.com/tutorial/body/)
- [FastAPI response model](https://fastapi.tiangolo.com/tutorial/response-model/)
- [Pydantic fields](https://docs.pydantic.dev/latest/concepts/fields/)
- [Pydantic models](https://docs.pydantic.dev/latest/concepts/models/)
