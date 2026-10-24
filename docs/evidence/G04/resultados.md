# G04 — Resultados da sondagem da Open Library

## Execução

- Data: 24/10/2026, das 12:37 às 13:00 (horário de Brasília).
- Modo: consultas manuais ao vivo, sem coleta em massa.
- Amostra: 13 consultas — 5 por título, 3 por autor, 3 por assunto e 2 de detalhe.
- Inspeção: três registros por busca, totalizando 33 ocorrências inspecionadas, além de uma obra e uma edição.
- Status HTTP: não verificados.
- Não foram observadas mensagens explícitas de erro nos JSONs recebidos.
- URLs, parâmetros e origem das consultas: [roteiro](roteiro.md).
- Respostas completas preservadas na pasta `responses/`.

## Consultas e cobertura observada

“Total” corresponde à contagem informada pela busca, não à quantidade de obras distintas confirmadas. Todas as buscas retornaram três registros e informaram `numFoundExact: true`.

| ID | Hora | Consulta | Total | Resultado da inspeção | Evidência |
| --- | --- | --- | --- | --- | --- |
| Q01 | 12:37 | Ensaio sobre a Cegueira | 6 | Correspondência de título/autoria no primeiro registro; campos ausentes nos demais. | [JSON](responses/Q01.json) |
| Q02 | 12:45 | O Cortiço | 27 | Resultados pertinentes com variações do nome do autor; dados incompletos. | [JSON](responses/Q02.json) |
| Q03 | 12:47 | Quarto de Despejo | 5 | Primeiro e terceiro atribuídos a Carolina Maria de Jesus; segundo atribuído a Jonathan C. Young. | [JSON](responses/Q03.json) |
| Q04 | 12:48 | A Metamorfose | 28 | Dois registros atribuídos a Kafka; terceiro sem autoria; anos diferentes. | [JSON](responses/Q04.json) |
| Q05 | 12:49 | Conceição Evaristo | 17 | Três títulos pertinentes, com nome completo ou abreviado da autora. | [JSON](responses/Q05.json) |
| Q06 | 12:50 | José Saramago | 726 | Três resultados com autoria correspondente. | [JSON](responses/Q06.json) |
| Q07 | 12:51 | Carolina Maria de Jesus | 44 | Três resultados com autoria correspondente, incluindo registro somente com idioma inglês. | [JSON](responses/Q07.json) |
| Q08 | 12:53 | Assunto: filosofia | 2798 | Resultados relacionados ao tema, incluindo obras associadas também a ciência e cosmologia. | [JSON](responses/Q08.json) |
| Q09 | 12:54 | Assunto: philosophy | 339844 | Resultados pertinentes, diferentes dos retornados em Q08. | [JSON](responses/Q09.json) |
| Q10 | 12:55 | Assunto: literatura brasileira | 322 | Três registros com o assunto solicitado; um apresenta título em francês. | [JSON](responses/Q10.json) |
| Q11 | 12:58 | Detalhe da obra Quarto de Despejo | Não se aplica | Obra identificada, primeira publicação registrada como 1960 e descrição em inglês. | [JSON](responses/Q11.json) |
| Q12 | 12:59 | Detalhe de uma edição de Quarto de Despejo | Não se aplica | Edição em português, de 1993, vinculada à obra de Q11; descrição ausente. | [JSON](responses/Q12.json) |
| Q13 | 13:00 | Fahrenheit 451 | 86 | Primeiro registro pertinente; demais incluem título composto e obra de outra autora. | [JSON](responses/Q13.json) |

## Idiomas observados

Nas buscas, `language` informa idiomas associados às edições da obra. No detalhe da edição, `languages` identifica o idioma daquele registro.

Códigos destacados nesta análise: `por` = português, `eng` = inglês e `fre` = francês. As listas completas permanecem nos JSONs.

| Consultas | Observação |
| --- | --- |
| Q01 e Q02 | Primeiro registro inclui português e outros idiomas; nos demais, `language` está ausente. |
| Q03 | Primeiro informa inglês e português; terceiro informa português; segundo sem `language`. |
| Q04 | Segundo informa português; primeiro e terceiro sem `language`. |
| Q05 | Os três registros informam português. |
| Q06 | Os três incluem português, acompanhado de outros idiomas. |
| Q07 | Primeiro informa inglês e português; segundo somente inglês; terceiro somente português. |
| Q08 | Português aparece somente no segundo registro; os demais informam outros idiomas. |
| Q09 | Os três informam idiomas, mas nenhum inclui português. |
| Q10 | Os três incluem português; o terceiro apresenta título em francês e informa francês e português. |
| Q11 | Título em português, descrição em inglês e ausência de campo estruturado de idiomas nessa resposta da obra. |
| Q12 | Edição identificada como português por `/languages/por`. |
| Q13 | Primeiro inclui português e outros idiomas; segundo e terceiro informam somente inglês. |

### Implicações para o CAPITU

- Pesquisar em português não restringe automaticamente os resultados a esse idioma.
- O idioma do título ou da descrição pode diferir dos idiomas associados às edições.
- Campo de idioma ausente significa informação não retornada, não inexistência de edição em português.
- A presença de `por` não comprova acesso ao texto integral.
- A amostra não permite prometer cobertura universal em português.

## Campos e formatos relevantes

### Busca

Foram inspecionados seis campos solicitados por consulta de busca, registrando sua presença ou ausência.

| Campo | Informação observada |
| --- | --- |
| `key` | Identificador do registro da obra. |
| `title` | Título apresentado pela fonte. |
| `author_name` | Lista de nomes associados à autoria. |
| `first_publish_year` | Ano informado pela fonte; sem validação histórica nesta sondagem. |
| `language` | Lista de códigos de idiomas associados às edições. |
| `edition_count` ou `subject` | Contagem de edições nas buscas por título/autor, ou assuntos nas buscas temáticas. |

### Ausências e particularidades

As posições abaixo correspondem à ordem recebida nos JSONs.

| Consulta | Registro | Observação |
| --- | --- | --- |
| Q01 | Segundo | Ausentes: `first_publish_year` e `language`. |
| Q01 | Terceiro | Ausentes: `author_name`, `first_publish_year` e `language`. |
| Q02 | Segundo e terceiro | Ausentes: `first_publish_year` e `language`. |
| Q03 | Segundo | `language` ausente; autoria diferente da procurada. |
| Q04 | Primeiro | `language` ausente. |
| Q04 | Terceiro | Ausentes: `author_name` e `language`. |
| Q05–Q10 e Q13 | Todos os três | Os seis campos solicitados estão presentes; presença não garante correção bibliográfica. |

Todos os campos identificados como ausentes foram solicitados nas URLs. A ausência na busca não comprova ausência no endpoint de detalhe.

Valores como `edition_count: 0` são informações presentes e não devem ser tratados como campos ausentes. Da mesma forma, uma lista de autores presente não confirma, sozinha, o papel bibliográfico de cada nome.

### Obra e edição

| Informação | Obra Q11 | Edição Q12 |
| --- | --- | --- |
| ID | `/works/OL1810404W` | `/books/OL46864874M` |
| Tipo | `/type/work` | `/type/edition` |
| Data | `first_publish_date: 1960` | `publish_date: 1993` |
| Autoria | `authors[].author.key` | `authors[].key` |
| ID de autoria | `/authors/OL217145A` | `/authors/OL217145A` |
| Descrição | Objeto com `type`/`value`; texto em inglês | Ausente |
| Idioma estruturado | Não retornado | `/languages/por` |
| ISBNs | Não retornados | `isbn_10` e `isbn_13` presentes |

Q12 referencia Q11 em `works[0].key`. A edição informa editora `Atica`, 202 páginas e ISBNs `8508105312` e `9788508105311`. Seu objeto `identifiers` está vazio, apesar dos ISBNs presentes em campos próprios.

## Achados para a E08

- Conferir título, autoria e ID: Q03 e Q13 retornam candidatos que não devem ser selecionados automaticamente como a obra procurada.
- Tratar campos ausentes sem inventar valores; distinguir ausência, objeto vazio e valor zero.
- Normalizar formatos diferentes: `author_name` na busca, `authors[].author.key` na obra e `authors[].key` na edição.
- Preservar a relação entre obra e edição e suas datas específicas.
- Considerar a descrição da obra quando estiver ausente na edição, preservando a origem e o idioma do texto.
- Observar a influência do vocabulário: `filosofia` e `philosophy` retornaram conjuntos e contagens diferentes. Mais resultados não comprovam maior pertinência.
- Apresentar datas com cautela: Q02 retorna 1925 para O Cortiço; Q04 retorna 2017 e 2016 para registros atribuídos a Kafka. São valores recebidos, sem validação histórica nesta sondagem.

## Validação dos roteiros

| Roteiro | Evidências | Situação |
| --- | --- | --- |
| API-01 — Título | Q01–Q04 e Q13 | Executado; correspondências pertinentes encontradas |
| API-02 — Autor | Q05–Q07 | Executado; resultados pertinentes encontrados |
| API-03 — Assunto | Q08–Q10 | Executado; diferenças de vocabulário e idioma registradas |
| API-04 — Detalhe | Q11–Q12 | Executado; relação entre obra e edição confirmada |
| API-05 — Campo ausente | Q01–Q04 e Q12 | Executado; ausências reais identificadas |

## Limites da análise

A sondagem avalia os metadados recebidos diretamente da Open Library, não o funcionamento do chatbot CAPITU.

Não houve falha técnica explícita nos conteúdos recebidos, mas os status HTTP não foram verificados. Campos ausentes e candidatos pouco pertinentes foram tratados como limitações dos dados ou da recuperação, sem atribuí-los a falhas da aplicação.

A amostra não comprova cobertura universal em português, correção histórica de todas as datas, disponibilidade de texto integral ou acervo institucional. Registros semelhantes não foram classificados automaticamente como duplicatas.