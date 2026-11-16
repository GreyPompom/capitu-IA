# E11 — resultado da avaliação de PLN

Execução: **16/11/2026**  
Modo: offline, determinístico e sem rede.  
Treino: `data/splits/reference.csv` (84 exemplos).  
Teste reservado: `data/splits/test.csv` (18 exemplos). O arquivo de teste não foi usado para ajustar o índice, limiar ou regras.

## Métricas de intenção

| Medida | Resultado |
| --- | ---: |
| Accuracy geral | 44,44% (8/18) |
| Macro precision | 75,00% |
| Macro recall | 45,00% |
| Macro F1 | 55,56% |
| Fallback/abstenção | 55,56% (10/18) |

| Intenção | Precision | Recall | F1 | Suporte |
| --- | ---: | ---: | ---: | ---: |
| `buscar_por_titulo` | 0,00% | 0,00% | 0,00% | 5 |
| `buscar_obras_autor` | 100,00% | 50,00% | 66,67% | 4 |
| `buscar_por_assunto` | 100,00% | 80,00% | 88,89% | 5 |
| `consultar_detalhes` | 100,00% | 50,00% | 66,67% | 4 |

## Matriz de confusão

Linhas = intenção esperada; colunas = saída prevista. `fallback` inclui rejeição e ambiguidade, portanto não foi removido do denominador.

| Esperada \ Prevista | Título | Autor | Assunto | Detalhes | Fallback |
| --- | ---: | ---: | ---: | ---: | ---: |
| Título | 0 | 0 | 0 | 0 | 5 |
| Autor | 0 | 2 | 0 | 0 | 2 |
| Assunto | 0 | 0 | 4 | 0 | 1 |
| Detalhes | 0 | 0 | 0 | 2 | 2 |

## Parâmetros e comportamento negativo

| Medida | Resultado | Observação |
| --- | ---: | --- |
| Entidade principal | 100,00% (16/16) | Extração medida com a intenção esperada para isolá-la do classificador. |
| Campo solicitado | 100,00% (4/4) | Rótulos do dataset foram convertidos ao contrato interno. |
| Contexto de sessão | 2 casos separados | `G01-037` e `G01-039` exigem resultado anterior; não entram no denominador de entidade direta. |
| Negativos/ambíguos G02 | 100,00% (20/20) | Fora do escopo e pedido de esclarecimento no fluxo sem sessão. |

## Interpretação

O resultado não prova compreensão geral de língua portuguesa. O sistema foi conservador: não houve falso aceite entre as oito intenções aceitas, mas muitas reformulações inéditas foram abstidas. A principal ação posterior é ampliar o corpus **em nova versão**, sem mover o atual teste reservado para treino; qualquer melhoria deve ser medida em um novo conjunto independente.

O resultado estruturado, incluindo hashes dos splits, previsões individuais e métricas completas, está em [`e11_intent_metrics.json`](e11_intent_metrics.json).
