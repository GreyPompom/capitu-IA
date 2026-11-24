# E12 — Diagnóstico técnico de falhas reais

Esta análise usa falhas efetivamente registradas em G05, G06 e M05. Ela
distingue o comportamento histórico da situação após cada correção; não usa a
variação da Open Library como prova de inexistência de uma obra.

## E12-01 — Paráfrase de título rejeitada

| Campo | Registro |
| --- | --- |
| Evidência original | G05 T03, em 10/11/2026: `Estou atrás de um livro chamado 1984`. |
| Esperado | Intenção `buscar_por_titulo`, entidade `1984` e busca controlada por título. |
| Obtido originalmente | `awaiting_clarification`, sem intenção aceita e sem chamada ao catálogo. |
| Causa técnica | A formulação não tinha sinal de alta precisão no interpretador e não possuía padrão específico de extração de título. |
| Impacto | Uma forma natural de busca por obra não chegava à Open Library. |
| Correção aplicada | Regra geral para `estou atrás de um livro chamado` em `nlp/interpretation.py` e `TITLE_PATTERNS` em `nlp/entity_extraction.py`. |
| Regressão | `test_g05_search_variations_use_exact_catalog_parameter` e `test_g05_title_author_subject_and_detail_variations_extract_exact_entities`. |
| Comparação honesta | Falhou na G05 histórica; passou 3/3 na G06 controlada e integra o resultado G05 fixture 24/24. |

## E12-02 — Comando incluído indevidamente no assunto

| Campo | Registro |
| --- | --- |
| Evidência original | G05 T09, em 10/11/2026: `Me mostre ficção científica`. |
| Esperado | Intenção `buscar_por_assunto` e parâmetro `ficção científica`. |
| Obtido originalmente | A busca recebeu `Me mostre ficção científica`; no modo ao vivo histórico retornou lista vazia. |
| Causa técnica | O extrator não isolava o trecho posterior ao comando `mostre`; o fallback preservava a frase inteira. |
| Impacto | A API recebia uma consulta bibliográfica degradada e podia retornar resultado vazio incorreto para o usuário. |
| Correção aplicada | Padrão de assunto para `mostre [assunto]`, que extrai somente a entidade. |
| Regressão | `test_g05_search_variations_use_exact_catalog_parameter` e `test_g05_title_author_subject_and_detail_variations_extract_exact_entities`. |
| Comparação honesta | Falhou na G05 histórica; passou 3/3 na G06 controlada com a chamada `subject: ficção científica`. |

## E12-03 — Interface presa quando a requisição não responde

| Campo | Registro |
| --- | --- |
| Evidência original | M05-D01, UI-14, em 17/11/2026. |
| Esperado | Após resposta, erro **ou timeout**, o loading termina e controles são liberados. |
| Obtido originalmente | Com `fetch` que nunca resolve, `Consultando acervo...` persistia e a página precisava ser recarregada. |
| Causa técnica | A UI aguardava `fetch` sem prazo; assim, o bloco `finally`, responsável por remover o loading e reabilitar controles, nunca era executado. |
| Impacto | A conversa podia ficar inutilizável diante de rede travada ou servidor sem resposta. |
| Correção aplicada | `fetchWithTimeout` usa `AbortController` e `Promise.race` com limite de 15 segundos. O timeout cancela a requisição, exibe mensagem de nova tentativa e alcança o `finally`. |
| Regressão | `test_timeout_cancels_request_and_releases_the_ui_path` em `tests/test_static_ui_contract.py`. |
| Comparação honesta | A falha manual está preservada em M05. A regressão automatizada verifica a presença do cancelamento, limite, mensagem e limpeza. A confirmação visual após 15 s ainda deve ser registrada no navegador. |

## Prioridade e limites

| Prioridade | Item | Situação |
| --- | --- | --- |
| P0 | E12-03 — timeout da interface | Corrigido no código; aguarda aceite visual de 15 s. |
| P1 | E12-01 e E12-02 — variações de linguagem | Corrigidas e cobertas por regressão controlada. |
| P2 | Ampliar frases inéditas | Recomendado para evolução do corpus; não alegar que mede generalização independente. |

## Comandos de reprodução

```text
python scripts/run_g06_reproduction.py --repeats 3
python scripts/run_g05_acceptance.py --mode fixture
pytest -q tests/test_entity_extraction.py tests/test_chat_integration.py tests/test_static_ui_contract.py tests/test_main.py
```
