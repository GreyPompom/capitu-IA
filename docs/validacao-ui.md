# Registro de validação da interface

## Situação deste registro

As capturas desta pasta registram uma exploração manual anterior da interface com a fonte externa ativa. Elas mostram que a UI enviou mensagens a `POST /api/chat` e renderizou os estados recebidos, mas não são a evidência final de aceite da M03: a consulta de detalhes falhou naquela execução por uma lacuna de extração de título então registrada como `REG-001`.

Após a correção, a validação controlada de backend está automatizada em `tests/test_chat_integration.py`. A validação visual manual abaixo continua necessária porque envolve browser, aba Network, foco e observação da renderização.

## Evidências exploratórias anteriores

| Fluxo observado | Resultado registrado | Evidências |
| --- | --- | --- |
| Busca por título | A UI recebeu lista e exibiu candidatos. | `UI-05-resultados-parte-1.png`, `UI-05-resultados-parte-2.png` |
| Busca por autor | A UI exibiu corretamente o estado `no_results` retornado pela fonte externa. Isso não valida um resultado positivo de autor. | `UI-06-resultados.png` |
| Busca por assunto | A UI recebeu candidatos e apresentou pedido de seleção. | `UI-07-resultados-parte-1.png`, `UI-07-resultados-parte-2.png` |
| Detalhes | A UI enviou o pedido, mas o backend pediu novamente o título. A falha está registrada em `REG-001`; as capturas não podem ser usadas como aceite. | `UI-08-resultados-teste-1.png`, `UI-08-resultados-teste-2-parte-1.png`, `UI-08-resultados-teste-2-parte-2.png`, `UI-08-resultados-teste-3.png` |

## Validação manual pendente para aceite M03

Executar com a aplicação local, registrar data, commit, navegador, payload e screenshot. Marcar cada item como passou somente após observá-lo no browser.

| ID | Procedimento | Resultado esperado | Situação |
| --- | --- | --- | --- |
| M03-UI-01 | Enviar uma busca por título e olhar Network. | `POST /api/chat`; primeiro payload com `session_id: null`; texto, estado e resultados renderizados. | Pendente de validação humana |
| M03-UI-02 | Enviar uma segunda mensagem na mesma conversa, depois clicar em Nova conversa e enviar uma terceira. | Segundo payload reutiliza o UUID; após reinício o payload volta a usar `session_id: null`. | Pendente de validação humana |
| M03-UI-03 | Clicar em cartão de resultado por mouse e teclado. | A UI envia `Detalhes de “<título>”` pela mesma rota, preserva a sessão e não recebe pedido redundante de título. Se houver vários candidatos, apresenta seleção. | Pendente de validação humana |
| M03-UI-04 | Forçar resposta HTTP não-2xx e, separadamente, parar o servidor para provocar falha de rede. | HTTP mostra a mensagem de solicitação recusada; rede mostra a mensagem de comunicação indisponível; em ambos o loading termina e o envio é reabilitado. | Pendente de validação humana |

## Limites

As verificações automáticas usam catálogo fake e não fazem chamadas à Open Library. Uma consulta ao vivo pode demonstrar conectividade, mas não substitui o conjunto controlado nem torna uma busca vazia prova de inexistência da obra.
