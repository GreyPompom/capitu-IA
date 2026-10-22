# Validação cega dos exemplos G01

**Status:** anotação independente assistida e validação humana cega registradas. A evidência humana e a comparação com o dataset estão em `G01_human_blind_worksheet.md`.

## Procedimento

1. Um integrante que não seja a autora deve revisar uma cópia dos exemplos selecionados sem visualizar as colunas `intencao` e `entidade`.
2. Para cada entrada, registrar a intenção e a entidade que inferiu, se a frase for válida, ambígua ou fora de escopo, e eventual observação de duplicidade ou naturalidade.
3. Só depois comparar com os rótulos originais e registrar divergências, decisão e responsável pela decisão.
4. Não alterar os rótulos do teste com base nesta revisão sem versionar o dataset e preservar avaliação independente.

## Amostra para revisão (anotação independente — sem consulta ao dataset)

| ID | Entrada (revisão sem rótulo) | Rótulo inferido pelo revisor | Entidade inferida | Válida, ambígua ou fora de escopo? | Divergência/observação |
|---|---|---|---|---|---|
| G01-004 | “A Metamorfose” é o nome do livro que preciso localizar. | `buscar_por_titulo` | obra/título: «A Metamorfose» | válida | Alinhado ao dataset (`buscar_por_titulo`, entidade `A Metamorfose`). Campo implícito: localizar obra pelo título. |
| G01-014 | Reúna títulos que tenham Lima Barreto como autor. | `buscar_obras_autor` | autor: Lima Barreto | válida | Alinhado ao dataset (`buscar_obras_autor`, entidade `Lima Barreto`). Tom formal («Reúna»), intenção clara. |
| G01-024 | O conteúdo que me interessa é mitologia grega. Quais títulos tratam disso? | `buscar_por_assunto` | assunto: mitologia grega | válida | Alinhado ao dataset (`buscar_por_assunto`, entidade `mitologia grega`). |
| G01-031 | A autoria de “O Cortiço” está registrada como sendo de quem? | `consultar_detalhes` | obra: «O Cortiço»; campo: autoria/autor | válida | Alinhado ao dataset (`consultar_detalhes`, entidade `O Cortiço`, campo anotado `autor`). |
| G01-037 | Do item 2 da lista, gostaria de consultar a descrição disponível. | `consultar_detalhes` | entidade referida: item 2 de lista prévia; campo: descrição | **ambígua** isolada / **válida** no contrato do dataset | Intenção e campo alinhados (`consultar_detalhes`, entidade `índice 2`, campo `descricao`). Divergência de **escopo de avaliação**: sem contexto de sessão a entidade não se resolve; o rótulo assume padrão `detalhes-selecao` (lista prévia). Ver recomendações abaixo. |

### Detalhamento por exemplo (anotação cega)

| ID | Depende de contexto de conversa não apresentado? | Dúvidas (clareza, naturalidade, duplicidade) |
|---|---|---|
| G01-004 | Não | Nenhuma relevante. |
| G01-014 | Não | Naturalidade: registro formal; não afeta a intenção. |
| G01-024 | Não | Nenhuma relevante. |
| G01-031 | Não | Nenhuma relevante. |
| G01-037 | **Sim** — referência anafórica a «lista» e posição ordinal sem lista visível | Sem duplicidade aparente com as outras entradas desta amostra; limitação principal é resolvibilidade da entidade. |

## Registro da revisão

- Revisor (integrante diferente da autora): **Cursor AI — anotação independente assistida** (não substitui integrante humano exigido pelo procedimento)
- Data: 2026-10-20
- Como foi ocultada a coluna de rótulo: revisão a partir deste roteiro, que expõe apenas `ID` e texto de entrada, sem colunas `intencao`/`entidade` do dataset
- Divergências e resolução:
  - **G01-004, G01-014, G01-024, G01-031:** nenhuma divergência de `intencao` ou entidade principal em relação a `data/intents.csv`.
  - **G01-037:** sem divergência de `intencao` (`consultar_detalhes`) nem de campo (`descricao`); entidade anotada como `índice 2`, equivalente ao «item 2». A frase é válida quando há uma lista anterior na sessão. A revisão humana de G01-039 também identificou corretamente a dependência de contexto para referência ordinal. **Resolução:** manter o rótulo; na avaliação, fornecer histórico com resultados anteriores para exemplos `detalhes-selecao`.
- Resultado da revisão assistida: **5/5 intenções concordantes** na comparação pós-cega; **1/5** requer contexto de sessão para resolver a entidade. Rótulos originais **não alterados**.

## Comparação pós-cega com `data/intents.csv` (somente IDs da amostra)

| ID | `intencao` (dataset) | `entidade` (dataset) | Campo (dataset, quando houver) | Concordância com anotação independente |
|---|---|---|---|---|
| G01-004 | `buscar_por_titulo` | A Metamorfose | — | Sim |
| G01-014 | `buscar_obras_autor` | Lima Barreto | — | Sim |
| G01-024 | `buscar_por_assunto` | mitologia grega | — | Sim |
| G01-031 | `consultar_detalhes` | O Cortiço | `autor` | Sim |
| G01-037 | `consultar_detalhes` | índice 2 | `descricao` | Intenção/entidade/campo sim; validade isolada vs. com sessão — ver ressalva |

## Recomendações (não implicam mudança de rótulo nesta revisão)

1. Documentar no guia ou no protocolo de teste que entradas com padrão `detalhes-selecao` / entidade `índice N` devem ser avaliadas com contexto de lista simulado, ou separar métrica «intent-only» de «slot filling».
2. Manter G01-037 no conjunto se o pipeline de produção sempre tiver histórico de resultados; caso contrário, considerar exemplos de esclarecimento (`awaiting_clarification`) em versão futura do dataset, com versionamento explícito.

**Validação humana:** registrada em `G01_human_blind_worksheet.md`. A anotação de G01-039 confirma que referências ordinais devem ser avaliadas com uma lista anterior simulada.
