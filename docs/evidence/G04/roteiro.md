# G04 — Roteiro de sondagem da Open Library

## Objetivo

Verificar a cobertura da Open Library para consultas bibliográficas da CAPITU, registrando resultados reais, idiomas, campos disponíveis e limitações para apoiar a E08.

Status: 13 consultas executadas; resultados registrados em resultados.md.

## Procedimento

1. Executar manualmente cada URL no navegador, uma por vez.
2. Aguardar pelo menos cinco segundos entre as consultas.
3. Limitar as buscas a três registros, sem coleta em massa ou paginação.
4. Salvar cada resposta JSON original em `responses/QXX.json`.
5. Registrar os resultados em `resultados.md`, incluindo data, horário, URL, status HTTP observado, contagens, IDs, campos e idiomas.
6. Examinar todos os registros retornados na página limitada.
7. Distinguir resultados pertinentes, limitações de cobertura, dados ausentes e falhas técnicas.
8. Não alterar respostas reais nem inventar informações ausentes.

O intervalo de cinco segundos é uma escolha desta sondagem.
Os limites oficiais serão documentados na ficha da API.

Serão executadas 13 consultas iniciais. Até duas consultas adicionais
poderão ser realizadas, se necessárias, com justificativa registrada.

## Roteiros de validação

| ID | Tipo | Procedimento | O que registrar |
| --- | --- | --- | --- |
| API-01 | Título | Executar Q01 a Q04 e Q13, e conferir título e autoria dos candidatos | Correspondência, IDs, campos e idiomas |
| API-02 | Autor | Executar Q05 a Q07 e conferir a autoria dos livros retornados | Pertinência das obras, IDs e campos |
| API-03 | Assunto | Executar Q08 a Q10 e comparar os resultados dos temas | Pertinência, vocabulário e idiomas |
| API-04 | Detalhe | Executar Q11 e Q12 e comparar obra e edição | Referência entre IDs, datas e campos específicos |
| API-05 | Campo ausente | Inspecionar as respostas, especialmente os detalhes Q11/Q12 | Campo relevante ausente, nulo ou vazio e impacto para o CAPITU |

API-05 pode utilizar uma resposta já obtida nos demais roteiros.
Se não houver um exemplo adequado, selecionar uma consulta adicional e registrar a justificativa, respeitando o máximo de 15 consultas.

## Consultas planejadas

### Q01 — Ensaio sobre a Cegueira

- Roteiro: API-01.
- Origem: G01-001.
- Verificação: procurar candidatos correspondentes ao título e conferir autoria.

https://openlibrary.org/search.json?title=Ensaio%20sobre%20a%20Cegueira&limit=3&fields=key,title,author_name,first_publish_year,language,edition_count

### Q02 — O Cortiço

- Roteiro: API-01.
- Origem: G01-002.
- Verificação: procurar candidatos correspondentes ao título e conferir autoria.

https://openlibrary.org/search.json?title=O%20Corti%C3%A7o&limit=3&fields=key,title,author_name,first_publish_year,language,edition_count

### Q03 — Quarto de Despejo

- Roteiro: API-01.
- Origem: G01-003.
- Verificação: procurar candidatos correspondentes ao título e conferir autoria.

https://openlibrary.org/search.json?title=Quarto%20de%20Despejo&limit=3&fields=key,title,author_name,first_publish_year,language,edition_count

### Q04 — A Metamorfose

- Roteiro: API-01.
- Origem: G01-004.
- Verificação: identificar registros da obra de Franz Kafka e possíveis homônimos.

https://openlibrary.org/search.json?title=A%20Metamorfose&limit=3&fields=key,title,author_name,first_publish_year,language,edition_count

### Q05 — Conceição Evaristo

- Roteiro: API-02.
- Origem: G01-011.
- Verificação: conferir se as obras retornadas são atribuídas à autora.

https://openlibrary.org/search.json?author=Concei%C3%A7%C3%A3o%20Evaristo&limit=3&fields=key,title,author_name,first_publish_year,language,edition_count

### Q06 — José Saramago

- Roteiro: API-02.
- Origem: G01-012.
- Verificação: conferir se as obras retornadas são atribuídas ao autor.

https://openlibrary.org/search.json?author=Jos%C3%A9%20Saramago&limit=3&fields=key,title,author_name,first_publish_year,language,edition_count

### Q07 — Carolina Maria de Jesus

- Roteiro: API-02.
- Origem: G01-018.
- Verificação: conferir se as obras retornadas são atribuídas à autora.

https://openlibrary.org/search.json?author=Carolina%20Maria%20de%20Jesus&limit=3&fields=key,title,author_name,first_publish_year,language,edition_count

### Q08 — Filosofia

- Roteiro: API-03.
- Origem: texto de G01-026.
- Verificação: observar a cobertura do assunto escrito em português.

https://openlibrary.org/search.json?q=subject%3Afilosofia&limit=3&fields=key,title,author_name,first_publish_year,language,subject

### Q09 — Philosophy

- Roteiro: API-03.
- Origem: comparação técnica com o tema de Q08.
- Verificação: observar diferenças ao pesquisar o mesmo tema em inglês.
- Observação: esta comparação não implementa tradução no CAPITU.

https://openlibrary.org/search.json?q=subject%3Aphilosophy&limit=3&fields=key,title,author_name,first_publish_year,language,subject

### Q10 — Literatura brasileira

- Roteiro: API-03.
- Origem: G01-028.
- Verificação: observar a pertinência dos resultados para o assunto.

https://openlibrary.org/search.json?q=subject%3A%22literatura%20brasileira%22&limit=3&fields=key,title,author_name,first_publish_year,language,subject

### Q11 — Detalhe da obra Quarto de Despejo

- Roteiros: API-04 e inspeção para API-05.
- Origem: obra utilizada no G01 e na G03.
- Verificação: examinar os campos da obra, especialmente autoria, descrição e primeira publicação, quando disponíveis.

https://openlibrary.org/works/OL1810404W.json

### Q12 — Detalhe de uma edição de Quarto de Despejo

- Roteiros: API-04 e inspeção para API-05.
- Origem: edição utilizada na G03.
- Verificação: examinar referência à obra, data da edição, editora, idioma, páginas e ISBNs, quando disponíveis.

https://openlibrary.org/books/OL46864874M.json

### Q13 — Fahrenheit 451

- Roteiro: API-01.
- Origem: G01-009.
- Verificação: procurar candidatos correspondentes ao título e conferi a autoria de Ray Bradbury.

https://openlibrary.org/search.json?title=Fahrenheit%20451&limit=3&fields=key,title,author_name,first_publish_year,language,edition_count

## Critérios de análise

- Registrar o total encontrado separadamente da quantidade retornada.
- Não exigir ordem fixa em consultas ao vivo.
- Conferir título e autoria; um resultado homônimo pode ser outra obra.
- Registrar os códigos de idioma como recebidos.
- Distinguir idioma do título, idioma da descrição e idiomas das edições.
- Não interpretar ausência de `language` como ausência de edição em português.
- Não confundir ano de primeira publicação com data de uma edição.
- Não classificar como ausente um campo que não foi solicitado na busca.
- Avaliar campos considerando o tipo de registro: obra ou edição.
- Registrar campo ausente, nulo e lista vazia separadamente.
- Um retorno vazio não comprova inexistência universal da obra.
- Falhas de rede, HTTP 429 ou 5xx não comprovam falta de cobertura.
- Esta sondagem direta da fonte não avalia o funcionamento do chatbot.
- A amostra não permite prometer cobertura universal em português.

## Evidências previstas

- `resultados.md`: registro das consultas executadas e análise dos cinco roteiros.
- `responses/Q01.json` a `responses/Q12.json`: respostas reais preservadas.
- Respostas adicionais, se necessárias, identificadas como Q13 a Q15.
- `screenshots/`: evidências complementares, quando úteis.
- `ficha-api.md`: síntese de rotas, campos, cobertura, limites e licenciamento.

Se uma consulta falhar, registrar o erro e preservar a evidência disponível.
Não criar um JSON fictício para substituir uma resposta real que não foi obtida.

## Fontes oficiais para consulta

- Search API:
  https://openlibrary.org/dev/docs/api/search
- APIs e diretrizes de uso:
  https://openlibrary.org/developers/api
- Licenciamento:
  https://openlibrary.org/developers/licensing