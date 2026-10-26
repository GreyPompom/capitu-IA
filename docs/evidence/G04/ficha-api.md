# G04 — Ficha da API Open Library

## Identificação e finalidade

- Serviço: Open Library, iniciativa do Internet Archive.
- Endereço: https://openlibrary.org
- Finalidade no CAPITU: fornecer metadados para descoberta bibliográfica.
- Sondagem: 13 consultas manuais realizadas em 24/10/2026.
- Evidências: [roteiro](roteiro.md), [resultados](resultados.md) e respostas
  originais na pasta `responses/`.

A API fornece dados bibliográficos. A interpretação das perguntas continua sendo responsabilidade do mecanismo de PLN do CAPITU.

## Rotas consultadas

| Finalidade | Método e rota | Parâmetros utilizados |
| --- | --- | --- |
| Buscar por título | GET /search.json | title, limit, fields |
| Buscar obras por autor | GET /search.json | author, limit, fields |
| Buscar por assunto | GET /search.json | q=subject:termo, limit, fields |
| Consultar obra | GET /works/{ID}.json | Identificador de obra |
| Consultar edição | GET /books/{ID}.json | Identificador de edição |

As buscas utilizaram `limit=3` e seleção explícita de campos.
A sondagem não utilizou autenticação nem chave de API.

## Campos e formatos observados

| Informação | Busca | Detalhe de obra | Detalhe de edição |
| --- | --- | --- | --- |
| Identificador | key | key | key |
| Título | title | title | title |
| Autoria | author_name: lista de nomes | authors[].author.key | authors[].key |
| Primeira publicação | first_publish_year | first_publish_date | Não confundir com publish_date |
| Publicação da edição | Não inspecionada | Não se aplica | publish_date |
| Idiomas | language: lista de códigos | Não retornados em Q11 | languages[].key |
| Assuntos | subject, quando solicitado | subjects | Não retornados em Q12 |
| Descrição | Não solicitada | description com type/value em Q11 | Ausente em Q12 |
| ISBNs | Não solicitados | Não retornados em Q11 | isbn_10 e isbn_13 |
| Editora e páginas | Não solicitadas | Não retornadas em Q11 | publishers e number_of_pages |

Os formatos acima foram observados na amostra; não representam garantia de presença em todos os registros.

Em Q11, a descrição está em `description.value`.
As referências de autoria dos detalhes fornecem IDs, não nomes diretamente. O serviço deverá resolver esses dados quando necessário.

## Cobertura observada

| Categoria | Consultas | Resultado |
| --- | --- | --- |
| Título | Q01–Q04 e Q13 | Encontradas correspondências pertinentes, junto de registros semelhantes ou relacionados. |
| Autor | Q05–Q07 | Encontrados livros com autoria correspondente, incluindo variações do nome. |
| Assunto | Q08–Q10 | Encontrados resultados relacionados aos temas, com diferenças de vocabulário e idioma. |
| Detalhe | Q11–Q12 | Obra e edição obtidas, com vínculo explícito entre seus IDs. |
| Campo ausente | Q01–Q04 e Q12 | Ausências reais observadas na busca e no detalhe da edição. |

A busca por `filosofia` retornou 2798 resultados; `philosophy`, 339844. A diferença não comprova maior pertinência nem equivalência entre os conjuntos.

Foram inspecionadas 33 ocorrências nas buscas e dois registros de detalhe. As contagens totais não foram tratadas como quantidade confirmada de obras originais e distintas.

## Idioma e qualidade dos dados

- Uma consulta em português pode retornar títulos e metadados em outros idiomas.
- `por` informa português entre os idiomas associados ao registro; não comprova acesso ao texto integral.
- A descrição de Quarto de Despejo em Q11 está em inglês, enquanto a edição Q12 está identificada como português.
- Ausência de idioma não comprova inexistência de edição em português.
- Campos de ano podem exigir conferência bibliográfica: os valores recebidos foram preservados, sem validação histórica.
- Títulos semelhantes e variações de autoria exigem seleção cuidadosa.
- Não há garantia de cobertura universal em português.

Segundo a documentação da Search API, `lang` influencia a preferência de idioma, mas não equivale a um filtro obrigatório. Esse parâmetro não foi utilizado nas 13 consultas.

## Limites e diretrizes de uso

Documentação oficial consultada em 24/10/2026:

- Limite padrão informado: 1 requisição por segundo.
- Requisições identificadas: 3 requisições por segundo.
- Identificar a aplicação por User-Agent contendo nome e contato,
  conforme as orientações oficiais.
- Utilizar cache quando possível e evitar consultas repetidas.
- Preferir endpoints JSON à extração de páginas HTML.
- Não utilizar a API para coleta em massa.

Nesta sondagem, as consultas foram executadas manualmente, em intervalos de minutos. Não foram realizados testes de carga, bloqueio, retentativas ou limites.

Os limites devem ser conferidos novamente durante a implementação e respeitados pelo conjunto de chamadas da aplicação.

## Licenciamento e uso dos dados

As condições de uso foram consultadas na [página oficial de licenciamento](https://openlibrary.org/developers/licensing). A sondagem utiliza uma pequena amostra de metadados com origem registrada; não se presume autorização para reutilizar textos integrais ou imagens associados aos registros.

## Limites da validação

Os JSONs recebidos não apresentaram mensagens explícitas de erro. Os status HTTP não foram registrados na sondagem original de 24/10/2026. Em conferência complementar de 26/10/2026, as 13 URLs retornaram 200 OK, conforme registro em resultados.md. Essa verificação não valida o funcionamento do chatbot nem garante disponibilidade contínua da fonte.

A sondagem direta da fonte não valida o cliente HTTP, a normalização, o PLN ou o funcionamento do chatbot. Também não comprova estoque institucional, disponibilidade de leitura ou estabilidade futura dos resultados.

## Referências oficiais

- Search API:
  https://openlibrary.org/dev/docs/api/search
- APIs, diretrizes e limites:
  https://openlibrary.org/developers/api
- Licenciamento:
  https://openlibrary.org/developers/licensing