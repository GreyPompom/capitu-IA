# Análise de erros

Este arquivo preserva falhas observadas e distingue o diagnóstico histórico da
situação após correção. Resultados de fonte externa não são tratados como
evidência de inexistência bibliográfica.

## REG-001 — Título não extraído em pedido de resumo

| Campo | Registro |
| --- | --- |
| Observação | 11/11/2026 — `quero ler o livro O pequeno principe, me de um resumo`. |
| Falha original | `consultar_detalhes` foi identificado, mas o título ficou nulo e o diálogo pediu esclarecimento. |
| Camada | Extração de entidades. |
| Correção | Padrão específico para “quero ler o livro [título], me dê um resumo”, sem quebrar referências de contexto. |
| Regressão | `test_detail_request_for_summary_extracts_title_and_description_field` e `test_summary_request_runs_controlled_detail_flow`. |
| Situação | **Corrigida e validada na M03 em 16/11/2026.** |

## Falhas iniciais da G05 — execução de 10/11/2026

A primeira execução de `scripts/run_g05_acceptance.py` registrou 17 aprovações e 7 falhas nas fixtures; no modo ao vivo, 16 aprovações, 7 falhas e T21 pendente. Esses resultados são históricos e orientam as correções abaixo. A reexecução final deve substituir os valores somente após o código e os oráculos serem revisados.

| Caso | Falha observada | Camada provável | Próxima ação |
| --- | --- | --- | --- |
| T03 | Paráfrase de busca por título foi abstida. | Intenção de título. | Cobrir “estou atrás de um livro chamado”. |
| T06 | Lista por autor foi abstida. | Intenção e extração de autor. | Cobrir “mostre obras de [autor]”. |
| T09 | Comando entrou no assunto enviado à API. | Extração de assunto. | Extrair somente “ficção científica”. |
| T10 | Paráfrase de assunto foi abstida. | Intenção e extração de assunto. | Cobrir “leitura a respeito de [assunto]”. |
| T12 | Pedido de detalhes foi abstido. | Intenção e extração de detalhes. | Cobrir “quero saber mais sobre [obra]”. |
| T16 | “um autor” virou assunto e consultou a fonte. | Validação de entidade obrigatória. | Pedir o nome do autor sem chamada externa. |
| T20 | Autor inexistente não alcançou a busca por autor. | Intenção de busca por autor. | Cobrir “obras de [autor]” com retorno vazio controlado. |

T21 permanece uma falha **injetada em fixture**; não se provoca indisponibilidade artificial contra a Open Library ao vivo.

## Reexecução controlada — 16/11/2026

Após as correções de intenção e extração, o comando abaixo foi executado sem rede:

```text
python scripts/run_g05_acceptance.py --mode fixture
```

Resultado: **24 de 24 casos passaram**. As regressões específicas também foram verificadas em `tests/test_entity_extraction.py` (1 teste) e `tests/test_chat_integration.py` (7 testes). A trilha ao vivo de 10/11 permanece no CSV como observação histórica da fonte externa; ela não é reescrita como se tivesse sido executada nesta versão.
