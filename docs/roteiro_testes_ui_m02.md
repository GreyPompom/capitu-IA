# Roteiro e registro de testes manuais de UI — M02

**Responsável pela tarefa:** Millena
**Ambiente previsto:** aplicação local FastAPI, servindo a interface em `/` e atendendo `POST /api/chat`
**Contrato:** `docs/contracts/chat-v1.md`
**Estado deste registro:** roteiro atualizado; resultados e capturas devem ser preenchidos após execução no navegador com o backend E02.

## Objetivo e contexto

Validar que a interface implementada em `static/` segue o contrato do chat, oferece os fluxos definidos no planejamento M02 e permanece utilizável por teclado. O backend E02 devolve dados demonstrativos; esses dados servem para integração de contrato, não comprovam busca real na Open Library nem interpretação por IA.

## Padrões de validação

- Executar os cenários no navegador com o backend local iniciado.
- Usar a aba Network para conferir método, URL, payload e resposta de `/api/chat`.
- Comparar campos com `ChatRequest` e `ChatResponse`: `message`, `session_id`, `text`, `state`, `results`; livros usam `title`, `authors`, `subjects` e `first_publish_year`.
- Registrar cada execução com data, navegador, resultado observado e screenshot em `docs/evidence/`.
- Marcar “Passou” somente após observar o comportamento. Em caso de falha, anotar evidência, abrir correção e repetir o caso.
- Usar dados simulados controlados para estados de lista vazia, item único, múltiplos resultados, API indisponível e conteúdo potencialmente malicioso.

## Casos de teste

| ID | O que cobre | Procedimento | Esperado | Resultado obtido | Situação |
|---|---|---|---|---|---|
| UI-01 | Envio válido e contrato | Enviar uma mensagem e inspecionar a requisição e resposta na aba Network. | Um `POST /api/chat` com `message` e `session_id` nulo no primeiro turno; renderizar `text`, `state` e `results` recebidos. | A preencher na execução manual. | Pendente |
| UI-02 | Entrada vazia | Enviar campo vazio e depois somente espaços. | Nenhuma requisição; mensagem acessível informa que é necessário digitar. | A preencher na execução manual. | Pendente |
| UI-03 | Carregamento e envio duplicado | Enviar durante uma resposta lenta e tentar enviar novamente. | Indicador de carregamento aparece; envio e atalhos ficam bloqueados até concluir; uma única requisição é enviada. | A preencher na execução manual. | Pendente |
| UI-04 | Zero, um e vários resultados | Simular respostas `results` vazia, com um livro e com múltiplos livros. | Exibir texto em todos os estados; cards aparecem apenas quando há resultados e preservam a ordem da API. | A preencher na execução manual. | Pendente |
| UI-05 | Reuso e reinício de sessão | Enviar duas mensagens; depois iniciar nova conversa e enviar novamente. | Reutilizar o UUID devolvido pelo backend no segundo turno; após reinício enviar `session_id: null`. | A preencher na execução manual. | Pendente |
| UI-06 | Metadados opcionais | Simular livro com autores/assuntos/ano e outro sem esses campos. | Mostrar apenas metadados presentes, sem texto “undefined”, falha ou quebra do card. | A preencher na execução manual. | Pendente |
| UI-07 | Ação no card | Acionar um card pelo mouse e pelo teclado. | Campo recebe pedido de detalhes do título e o fluxo envia uma nova solicitação; foco e nome acessível disponíveis. | A preencher na execução manual. | Pendente |
| UI-08 | Atalhos da barra lateral | Acionar cada atalho por clique e teclado. | O atalho correspondente preenche o campo e move o foco para a entrada. | A preencher na execução manual. | Pendente |
| UI-09 | Nova conversa | Acionar “Nova conversa” após troca de mensagens. | Histórico é limpo, mensagem de boas-vindas volta e sessão local é descartada. | A preencher na execução manual. | Pendente |
| UI-10 | API indisponível / erro HTTP | Parar backend ou simular resposta HTTP não bem-sucedida. | Remover carregamento, informar falha em linguagem clara, marcar conexão indisponível e permitir nova tentativa. | A preencher na execução manual. | Pendente |
| UI-11 | Conteúdo não confiável | Simular texto e título contendo marcação HTML/script. | Conteúdo é mostrado como texto; nenhum elemento ou script externo é executado. | A preencher na execução manual. | Pendente |
| UI-12 | Teclado e foco | Navegar com Tab e acionar com Enter/Espaço; observar foco. | Ordem previsível, foco visível e controles acionáveis sem mouse. | A preencher na execução manual. | Pendente |
| UI-13 | Rótulos e status acessíveis | Inspecionar nome do campo, anúncios de carregamento/erro e atualização da conexão. | Campo tem rótulo programático; estados são anunciados por regiões live/status. | A preencher na execução manual. | Pendente |
| UI-14 | Responsividade | Redimensionar viewport para desktop e largura menor que 768 px. | Layout adapta-se sem rolagem horizontal indevida e mantém controles operáveis. | A preencher na execução manual. | Pendente |
| UI-15 | Arquivos estáticos | Abrir `/` e verificar CSS, JS e imagens em Network. | Recursos carregam sob `/static/` sem 404 e a página inicial não apresenta erro JavaScript. | A preencher na execução manual. | Pendente |

## Evidências a guardar

Para cada cenário executado, preencher o resultado e situação na tabela, salvar screenshot em `docs/evidence/` com nome como `M02-UI-01.png` e registrar divergências em `docs/evaluation/error_analysis.md`. No teste UI-01, guardar também captura da requisição/resposta da aba Network sem dados pessoais.

## Limites da validação

O teste com backend E02 valida a integração da interface com o contrato e os dados simulados. A validação da busca real na Open Library, da classificação de intenções e da experiência final integrada depende das tarefas de backend correspondentes e deve ser registrada quando estiverem disponíveis.
