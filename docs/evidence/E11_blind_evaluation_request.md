# E11 — roteiro de validação cega independente

## Objetivo

Confirmar, com perguntas que a pessoa responsável pela implementação ainda não viu, que a CAPITU mantém o mínimo aceitável de 75% nas métricas de classificação.

Em termos simples: Miguel ou Millena escreve perguntas novas; Emely roda a CAPITU; só depois vocês comparam a resposta com o resultado esperado. Assim, ninguém consegue ajustar o código especificamente para essas perguntas antes do teste.

## Quem executa

Millena ou Miguel, de preferência quem **não** alterou `nlp/interpretation.py`. A pessoa que prepara as perguntas não deve consultar `data/splits/test.csv`, as previsões nem as regras antes de escrevê-las.

## Como preparar o conjunto

1. Criar 24 mensagens naturais e inéditas: 6 para cada intenção (`buscar_por_titulo`, `buscar_obras_autor`, `buscar_por_assunto`, `consultar_detalhes`). Esse total dá exemplos suficientes para observar cada fluxo, sem transformar o teste em uma tarefa longa.
2. Criar adicionalmente 8 mensagens: 4 fora do escopo e 4 ambíguas, com estado esperado correspondente.
3. Incluir formulações curtas, longas, sem acento, com sinônimos e pelo menos dois erros de digitação moderados.
4. Registrar somente a mensagem, a intenção/estado esperado, a entidade e, quando aplicável, o campo solicitado. Não consultar `data/splits/test.csv`, regras, resultados ou previsões para montar as frases.
5. Entregar a planilha para Emely executar. Não alterar os rótulos depois de ver a resposta do sistema. Esta etapa é recomendada para reforçar a defesa; não invalida a regressão já registrada.

## Modelo de registro

| ID | Entrada inédita | Intenção/estado esperado | Entidade | Campo solicitado | Resultado obtido | Passou? |
| --- | --- | --- | --- | --- | --- | --- |
| C01 |  |  |  |  |  |  |

## Critério de aceite

- Accuracy, Macro F1, F1 de cada intenção, entidade e campo solicitado: **>= 75%**.
- Casos fora do escopo/ambíguos: **>= 75%** de comportamento esperado.
- Fallback nas intenções positivas: **<= 25%**.

Após a execução, arquivar o CSV e o resultado em `evaluation/results/`, registrar os comandos em `docs/evidence/E11.md` e não sobrescrever nem a linha de base nem a regressão de desenvolvimento.
