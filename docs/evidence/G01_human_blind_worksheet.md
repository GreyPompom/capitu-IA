# Folha de anotação humana cega — G01

**Revisora:** Emely
**Data:** 2026-10-20

As interpretações foram registradas antes da comparação com `data/intents.csv` e sem consultar o relatório do Cursor. A comparação abaixo foi feita somente depois de concluir a anotação cega.

Para cada linha, anote a intenção que você entende, a entidade principal, o campo solicitado (se houver), se precisa de contexto anterior e qualquer dúvida. Use uma destas intenções quando fizer sentido: `buscar_por_titulo`, `buscar_obras_autor`, `buscar_por_assunto`, `consultar_detalhes`. Se não der para decidir com segurança, escreva “ambígua” e explique por quê.

| ID | Frase | Sua intenção | Entidade | Campo solicitado | Precisa de contexto? | Dúvida/observação |
|---|---|---|---|---|---|---|
| G01-006 | Minha próxima leitura já está escolhida: “Jane Eyre”. Localize esse livro. | `buscar_por_titulo` | “Jane Eyre” | titulo | nao | buscar livro por titulo |
| G01-018 | Estou reunindo referências de livros escritos por Carolina Maria de Jesus; pode listar os títulos? | `buscar_obras_autor` | Carolina Maria de Jesus | - | nao | busca obras da autora |
| G01-029 | A área que quero explorar nos livros é história da arte; localize obras sobre ela. | `buscar_por_assunto` | história da arte | - | nao | localizar obras por assunto |
| G01-034 | Sobre “O Nome da Rosa”, apresente as informações bibliográficas disponíveis. | `consultar_detalhes` | “O Nome da Rosa” | titulo | nao | buscar detalhes de um livro |
| G01-039 | No terceiro resultado, a autoria está atribuída a qual pessoa? | `consultar_detalhes` | terceiro resultado | autoria | sim | buscar o nome de uma pessoa no contexto |

## Resultado da comparação — preencher somente depois da anotação acima

| ID | Concorda com o dataset? | Divergência e decisão da equipe |
|---|---|---|
| G01-006 | Sim para intenção e entidade | `titulo` foi usado como critério de busca; o CSV deixa `campo_solicitado` vazio porque não há metadado bibliográfico pedido. Tratar título como entidade/critério, não como campo de resposta. |
| G01-018 | Sim | Intenção `buscar_obras_autor` e entidade `Carolina Maria de Jesus` correspondem; sem campo específico solicitado. |
| G01-029 | Sim | Intenção `buscar_por_assunto` e entidade `história da arte` correspondem; sem campo específico solicitado. |
| G01-034 | Parcial | Intenção e entidade correspondem. A anotação cega escreveu `titulo` como campo, mas a observação identifica corretamente um pedido de detalhes; o CSV usa `detalhes`. Decisão: manter o rótulo do dataset e registrar `detalhes` como campo consensual após comparação. |
| G01-039 | Sim, semanticamente | `terceiro resultado` equivale a `índice 3`; `autoria` equivale ao campo `autor`. Depende de resultados anteriores, como a revisora marcou. |

**Como os rótulos foram mantidos ocultos:** a anotação foi registrada nesta folha, que contém ID e texto, antes da comparação com `data/intents.csv`.
**Resultado final:** revisão humana cega concluída por Emely. As cinco intenções e entidades estão de acordo; os casos G01-006 e G01-034 exigiram harmonização entre critério de busca/campo solicitado. Nenhum rótulo do dataset foi alterado.
