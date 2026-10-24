# Fixtures

Respostas fictícias/controladas da Open Library para testes sem rede - G03

## Origem e modo

Modo: controlado. Exemplos montados manualmente com livros do G01
e identificadores conferidos no catálogo da Open Library.

Não são respostas integrais coletadas da API. Contagens e ordem foram definidas para os testes. O retorno vazio e a remoção de campos são simulações intencionais.

## Cenários e correspondência

| Arquivo | Cenário | Correspondência |
| --- | --- | --- |
| search_single.json | Um livro | G01-003 |
| search_multiple.json | Três livros para seleção | Pré-condição de G01-037 e G01-039 |
| search_empty.json | Nenhum resultado | Cenário adicional; apoio a T19/T20 |
| search_missing_fields.json | Campos opcionais ausentes | G01-002/G01-031 com dados reduzidos |
| edition.json | Edição específica | Cenário adicional de obra versus edição |

As correspondências indicam usos previstos, não diálogos já testados.

## Validação

Os testes verificam leitura dos JSONs, IDs, campos, tipos, contagens
e correspondência com os cenários, sem chamadas de rede.

Executar na raiz do projeto:

    python -m pytest tests/test_api_service.py -q


## Referências

- https://openlibrary.org/dev/docs/api/search
- https://openlibrary.org/books/OL46864874M
- https://openlibrary.org/works/OL1810404W
- https://openlibrary.org/works/OL1003134W
- https://openlibrary.org/works/OL103123W
- https://openlibrary.org/works/OL7058886W