# E11 — avaliação de PLN e métricas

Execução pós-correção: **16/11/2026**
Modo: offline, determinístico e sem rede.  
Treino: `data/splits/reference.csv` (84 exemplos).  
Avaliação: `data/splits/test.csv` (18 exemplos), que não participa da construção do índice TF-IDF.

## Resultado de regressão pós-correção

Após correções de padrões gerais de linguagem (título, obras de autor, assunto e detalhes), o mesmo conjunto reservado foi executado novamente para verificar regressão. O resultado completo, incluindo as duas mensagens que dependem de contexto, foi:

| Medida | Resultado | Meta interna mínima |
| --- | ---: | ---: |
| Accuracy geral | **88,89% (16/18)** | 75% |
| Macro precision | **100,00%** | 75% |
| Macro recall | **87,50%** | 75% |
| Macro F1 | **92,86%** | 75% |
| Menor F1 por intenção | **85,71%** | 75% |
| Fallback/abstenção | **11,11% (2/18)** | até 25% |
| Entidade principal | **100,00% (16/16)** | 75% |
| Campo solicitado | **100,00% (4/4)** | 75% |
| Negativos/ambíguos G02 | **100,00% (20/20)** | 75% |

| Intenção | Precision | Recall | F1 | Suporte |
| --- | ---: | ---: | ---: | ---: |
| `buscar_por_titulo` | 100,00% | 100,00% | 100,00% | 5 |
| `buscar_obras_autor` | 100,00% | 75,00% | 85,71% | 4 |
| `buscar_por_assunto` | 100,00% | 100,00% | 100,00% | 5 |
| `consultar_detalhes` | 100,00% | 75,00% | 85,71% | 4 |

No recorte de 16 mensagens independentes — isto é, removendo os dois casos cujo significado exige uma resposta anterior da sessão — a accuracy foi **93,75% (15/16)** e o Macro F1 foi **96,43%**. Esse recorte existe somente para diagnosticar o classificador isolado; a tabela anterior, de 18 linhas, é a métrica completa de regressão.

## Matriz de confusão da regressão completa

Linhas = intenção esperada; colunas = saída prevista. `fallback` inclui rejeição e ambiguidade e permanece no denominador.

| Esperada \\ Prevista | Título | Autor | Assunto | Detalhes | Fallback |
| --- | ---: | ---: | ---: | ---: | ---: |
| Título | 5 | 0 | 0 | 0 | 0 |
| Autor | 0 | 3 | 0 | 0 | 1 |
| Assunto | 0 | 0 | 5 | 0 | 0 |
| Detalhes | 0 | 0 | 0 | 3 | 1 |

## Rastreabilidade e limitação metodológica

A linha de base anterior — **44,44% (8/18)** de accuracy, Macro F1 **55,56%** e fallback **55,56%** — está preservada no commit `a47b898`, antes das correções. Ela revelou formulações que precisavam ser atendidas e orientou os ajustes posteriores.

Por esse motivo, o resultado desta página é uma **reavaliação de desenvolvimento/regressão**, não uma estimativa independente definitiva de generalização: o conjunto de 18 exemplos já foi visto durante a análise. Antes da entrega, Millena ou Miguel deve criar e executar o roteiro em [`docs/evidence/E11_blind_evaluation_request.md`](../../docs/evidence/E11_blind_evaluation_request.md), sem consultar `test.csv`, as previsões ou as regras. Só esse novo conjunto cego poderá ser apresentado como validação final independente.

O resultado estruturado contém hashes dos splits, previsões individuais, matriz de confusão e denominadores: [`e11_intent_metrics.json`](e11_intent_metrics.json).
