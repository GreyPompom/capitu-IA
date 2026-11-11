# Análise de erros

Registrar no mínimo três falhas observadas, com entrada, estado, esperado/obtido, camada provável, impacto, correção e teste de regressão. Não inventar resultados.

## Análise inicial G05 — fixtures e Open Library ao vivo, 2026-11-10

Os resultados completos e separados por proveniência estão em [`g05_acceptance.csv`](g05_acceptance.csv): 24 linhas com fixture determinística e 24 registros ao vivo. Na execução mais recente, fixtures: 17 passaram e 7 falharam; ao vivo: 16 passaram, 7 falharam e T21 ficou pendente. T21 exercita indisponibilidade apenas na fixture; não se provoca falha artificial contra a API real. As falhas abaixo também ocorreram ao vivo. T03 e T06 não chegaram a chamar a fonte; T09 fez uma consulta HTTP real com o assunto extraído incorretamente. As causas são hipóteses para investigação, não diagnósticos confirmados.

| Caso | Esperado | Observado | Camada provável e impacto | Próxima ação e regressão |
| --- | --- | --- | --- | --- |
| T03 — “Estou atrás de um livro chamado 1984” | Buscar título `1984`. | `awaiting_clarification`, sem intenção ou chamada HTTP; reproduzido na trilha ao vivo. | Reconhecimento/decisão de intenção: a paráfrase não chega à busca, independentemente da disponibilidade da fonte. | Inspecionar candidatos, scores e margem; registrar regressão da formulação e uma variante independente. |
| T06 — “Mostre obras de Clarice Lispector” | Buscar obras do autor `Clarice Lispector`. | `awaiting_clarification`, sem chamada HTTP; reproduzido na trilha ao vivo. | Reconhecimento da intenção de busca por autor. | Inspecionar ranking e extração; cobrir a intenção, o nome completo e a chamada correta ao catálogo em regressão. |
| T09 — “Me mostre ficção científica” | Buscar assunto `ficção científica`. | O motor aceitou busca por assunto, mas consultou `subject:Me mostre ficção científica`; a Open Library respondeu HTTP 200 sem resultados. | Extração da entidade: comando foi incluído no assunto e produziu consulta inadequada à fonte real. | Cobrir a entidade exata e validar intenção, parâmetro enviado e resposta com cliente controlado; não depender da ordenação/conteúdo ao vivo. |
| T16 — “Mostre livros de um autor” | Pedir o nome do autor, sem consultar o catálogo. | Classificou como assunto e consultou `subject:um autor`; a fonte real retornou um livro não relacionado. | Desambiguação/validação de parâmetro ausente: uma consulta bibliográfica sem entidade virou busca com parâmetro genérico. | Detectar entidade ausente antes da consulta e adicionar regressão HTTP que confira estado de esclarecimento e zero chamadas. |
