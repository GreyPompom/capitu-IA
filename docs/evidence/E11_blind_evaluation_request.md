# E11 — roteiro de validação cega independente

## Objetivo

Confirmar se a CAPITU mantém pelo menos 75% nas métricas de classificação sem reutilizar as frases que orientaram as regras de desenvolvimento.

## Quem executa

Millena ou Miguel, de preferência quem **não** alterou `nlp/interpretation.py`, `data/splits/test.csv` nem leu `evaluation/results/e11_intent_metrics.json`.

## Como preparar o conjunto

1. Criar 24 mensagens naturais e inéditas: 6 para cada intenção (`buscar_por_titulo`, `buscar_obras_autor`, `buscar_por_assunto`, `consultar_detalhes`).
2. Criar adicionalmente 8 mensagens: 4 fora do escopo e 4 ambíguas, com estado esperado correspondente.
3. Incluir formulações curtas, longas, sem acento, com sinônimos e pelo menos dois erros de digitação moderados.
4. Registrar somente a mensagem, a intenção/estado esperado, a entidade e, quando aplicável, o campo solicitado. Não consultar `data/splits/test.csv`, `data/splits/reference.csv`, regras, resultados ou previsões para montar as frases.
5. Entregar a planilha para Emely executar. Não alterar os rótulos depois de ver a resposta do sistema.

## Modelo de registro

| ID | Entrada inédita | Intenção/estado esperado | Entidade | Campo solicitado | Resultado obtido | Passou? |
| --- | --- | --- | --- | --- | --- | --- |
| C01 |  |  |  |  |  |  |

## Critério de aceite

- Accuracy, Macro F1, F1 de cada intenção, entidade e campo solicitado: **>= 75%**.
- Casos fora do escopo/ambíguos: **>= 75%** de comportamento esperado.
- Fallback nas intenções positivas: **<= 25%**.

Após a execução, arquivar o CSV e o resultado em `evaluation/results/`, registrar os comandos em `docs/evidence/E11.md` e não sobrescrever nem a linha de base nem a regressão de desenvolvimento.
