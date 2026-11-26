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

## Validação manual para aceite M03

Execução em 16/11/2026, com a aplicação local no commit `d55b524` e navegador integrado. A validação foi observada por Emely. As capturas e a confirmação humana estão registradas abaixo.

| ID | Procedimento | Resultado esperado | Situação |
| --- | --- | --- | --- |
| M03-UI-01 | Enviar uma busca por título e olhar Network. | `POST /api/chat`; primeiro payload com `session_id: null`; texto, estado e resultados renderizados. | **Passou.** Busca e cartões renderizados; chamadas `POST /api/chat` registradas no log local. |
| M03-UI-02 | Enviar uma segunda mensagem na mesma conversa, depois clicar em Nova conversa e enviar uma terceira. | Segundo payload reutiliza o UUID; após reinício o payload volta a usar `session_id: null`. | **Passou.** Emely confirmou reinício correto em “Nova conversa”. |
| M03-UI-03 | Clicar em cartão de resultado por mouse e teclado. | Com vários candidatos, a UI envia a posição correspondente, como `o segundo`, pela mesma rota; a resposta confirma a obra escolhida e mostra somente ela. Com um único resultado, envia `Detalhes de “<título>”`. | **Passou.** Seleção por mouse e por `Tab` + `Enter` confirmadas; autoria contextual exibida em `M03-UI-03-contexto-autoria-2026-11-16.png`. |
| M03-UI-04 | Forçar resposta HTTP não-2xx e, separadamente, parar o servidor para provocar falha de rede. | HTTP mostra a mensagem de solicitação recusada; rede mostra a mensagem de comunicação indisponível; em ambos o loading termina e o envio é reabilitado. | **Passou.** Fallback de rede observado em `M03-UI-04-fallback-rede-2026-11-16.png`; ramo HTTP não-2xx coberto por `tests/test_static_ui_contract.py`. |

## Limites

As verificações automáticas usam catálogo fake e não fazem chamadas à Open Library. Uma consulta ao vivo pode demonstrar conectividade, mas não substitui o conjunto controlado nem torna uma busca vazia prova de inexistência da obra.
