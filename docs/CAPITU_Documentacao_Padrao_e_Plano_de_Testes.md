# Documentação de testes e validação da CAPITU

> **Sincronização obrigatória: qualquer alteração neste documento deve ser reproduzida no PDF e no Markdown do mesmo nome-base antes do commit.**
> **PDF correspondente:** `CAPITU_Documentacao_Padrao_e_Plano_de_Testes.pdf`

## Documentação de testes e validação

Chatbot inteligente de descoberta bibliográfica • A3 de Inteligência Artificial • 7 de outubro de 2026

**Equipe:** Emely, Millena e Miguel • **Entrega:** 25/11/2026 • **Estado:** plano anterior à execução dos testes.

**Objetivo deste documento.** Definir o que a CAPITU precisa testar, o padrão usado para escrever e registrar casos, os níveis de teste, os critérios de aceite e a relação com as funcionalidades aprovadas. Os cenários esperados são especificações; nenhum resultado é alegado como já observado.

**Base consultada:** enunciado oficial A3, aula “Tecnologias possíveis e conceitos essenciais”, planejamento detalhado CAPITU e plano de tarefas da equipe. A proposta foi aprovada pelo professor segundo a informação da equipe. Datas/atribuições abaixo seguem o cronograma até 25/11.

## Leitura rápida: o que a equipe precisa entregar

| Obrigatório para a A3 | Planejado para CAPITU | Como evidenciar |
| --- | --- | --- |
| 20 ou mais perguntas de teste | 24 testes de aceitação T01-T24 com esperado, obtido e passou? | Tabela executada com versão, modo e estado inicial |
| Reformulações, ambiguidades e fora do escopo | Casos diretos, paráfrases, entidade ausente, typo, fallback e mudança de contexto | Suite congelada e regressões |
| Métricas compatíveis e análise de 3 falhas | Taxa de sucesso, classificação, matriz, fallback; fichas de falhas reais | Cálculos reproduzíveis e causas |
| Fluxo de entrada a resposta; abstenção | Unitário, diálogo, API controlada, UI, integração ponta a ponta | Automação pytest + tabela/roteiros manuais |
| Código/dados executáveis e autoria | Sem acesso à rede na suite padrão; instalação limpa; responsabilidades identificáveis | CI/local README e histórico de contribuição |

**Escopo funcional coberto:** buscar por título, buscar obras por autor, buscar por assunto/gênero, consultar detalhes; extração de título/autor/assunto; pergunta de esclarecimento; seleção de resultado; contexto mínimo; rejeição fora do escopo; Open Library pública; falha, retorno vazio, múltiplos resultados, campos ausentes e chat web local. Cache/mode técnico e capas/ISBN como busca são incrementos opcionais e não bloqueiam o MVP.

## 1. Padrão geral dos testes

Use uma especificação comum para que os três integrantes possam preparar, executar e revisar testes sem alterar o critério depois de observar o resultado.

| Campo de cada caso | O que registrar |
| --- | --- |
| ID e versão | ID estável; release/commit, configuração do interpretador e versão do dataset |
| Objetivo/camada | Qual componente e requisito a verificação cobre |
| Pré-condições | Sessão limpa ou estado prévio, fixtures, cache e dependências |
| Entrada/ação | Mensagem ou sequência exata; chamada interna ou ação de UI |
| Esperado/oráculo | Rótulo, entidade, decisão, chamada permitida e resultado visível, definidos antes |
| Obtido | Saída real, IDs/resposta e scores se diagnóstico ajudar; não reconstruir de memória |
| Resultado | Passou/falhou/bloqueado/não executado, com motivo e data |
| Modo | Unitário/mock, integrado controlado, manual ou smoke com API real |
| Evidência | Log, arquivo, screenshot ou referência ao output sem segredo |

### Padrão de escrita: Arrange, Act, Assert

**Arrange:** preparar sessão, corpus e fake da API. **Act:** chamar um componente ou enviar mensagem. **Assert:** verificar saída e também efeitos colaterais: score/decisão, entidade, estado de sessão e número de consultas. Um teste que verifica apenas que “não lançou exceção” é insuficiente para o comportamento esperado.

### Padrões técnicos adotados

- **Teste determinístico:** mesma entrada, fixture e versão produzem o mesmo resultado.

- **Test doubles:** fixture para retorno, mock/fake/spy para HTTP, relógio, cache e contagem de chamadas.

- **Sem rede por padrão:** unitários e testes de integração usam HTTP simulado; não depender de catálogo vivo.

- **Contrato explícito:** schemas de request/response, estado de ausência e erro diferentes, campos opcionais.

- **Teste de comportamento:** assert na decisão observável do usuário, além dos detalhes internos essenciais.

- **Independência:** teste começa com sessão/cache isolados, não depende da ordem de execução.

- **Um motivo principal por caso:** vários asserts coerentes são permitidos, mas falha deve apontar camada provável.

- **Dados controlados:** IDs e campos conhecidos; fixtures são marcadas como simulação, não resultado ao vivo.

- **Limite compartilhado:** rate limiter testa relógio falso, nunca faz loop de requisições reais para medir quota.

- **Regressão:** cada erro real escolhido para correção ganha caso repetível; versionar o que entrou no treino depois.

### Resultado do caso

**Passou:** o comportamento observado cumpre todo o oráculo. **Falhou:** comportamento diverge. **Bloqueado:** componente/dependência impede execução e há motivo. **Não executado:** sem tentativa. “Fallback correto” pode passar em entrada desconhecida; uma pergunta ambígua não deve receber rótulo único artificial.

## 2. O contexto geral e os padrões que os testes devem cobrir

| Área | Padrões do produto CAPITU | Pergunta de teste |
| --- | --- | --- |
| Intenções | buscar_por_titulo; buscar_obras_autor; buscar_por_assunto; consultar_detalhes | A ação pretendida foi reconhecida? |
| Entidades | Título, autor, assunto/gênero, identificador e campo solicitado | Parâmetro foi extraído completo e da entidade correta? |
| Semelhança lexical | TF-IDF/cosseno sobre frases de referência; scores não são probabilidade | Reconhece variante suportada sem exagerar a confiança? |
| Regra de decisão | Limiar + margem; aceita, esclarece ou abstém | Casos nos limites não disparam consulta errada? |
| Diálogo | Pendência, seleção numerada, item selecionado, cancelamento e nova demanda | Contexto curto permanece coerente e isolado por sessão? |
| Dados | Frases autorais/curadas, grupos de variação e splits | Teste está independente; não há vazamento de paráfrase? |
| Fonte externa | Open Library; obra/edição; campos incompletos | Consulta corresponde ao pedido; erros e limites são seguros? |
| Resposta | Templates só com dados disponíveis; origem visível | Resposta evita alegar acervo, completude ou dado ausente? |
| Interface | Chat web existente de Millena; execução local | Envio, espera, resultados e falhas são visíveis/utilizáveis? |
| Entrega/defesa | README, código, dados, resultados e contribuição individual | Outra pessoa executa? Cada integrante explica sua parte? |

### Quatro resultados de intenção não são quatro respostas iguais

**“Quais livros Machado escreveu?”** → buscar_obras_autor, entity author, lista. **“Quem escreveu Dom Casmurro?”** → consultar_detalhes, entity title, campo autor. O texto “escreveu” não decide sozinho. Testar o par junto para flagrar regras superficiais.

### Cobertura obrigatória da suite funcional

- Pergunta direta e paráfrase natural.

- Sinônimos/estrutura lexical variante e pequeno erro de grafia, com expectativa de sucesso ou esclarecimento definida.

- Ambiguidade e ausência de parâmetros.

- Fora do domínio e operação institucional fora do escopo.

- Livro/autor sem resultado na fonte simulada.

- API indisponível, timeout, limite HTTP, retorno múltiplo e campo ausente.

- Seleção de resultado e continuação curta; nova busca muda o contexto.

- Resultado de cada intenção e uma pergunta inédita na defesa.

**Regra de honestidade:** um teste de exemplo conhecido mede reprodução da referência. Generalização é medida pelo split independente, por paráfrases agrupadas corretamente e por reformulações inéditas; nenhum conjunto pequeno comprova cobertura geral da língua.

## 3. Camadas de teste e fronteiras

| Nível | Componente/foco | Rede | Executar quando | Dono primário |
| --- | --- | --- | --- | --- |
| Unitário - PLN | Normalização, TF-IDF, similaridade, limiar, margem e extração | Não | Em cada mudança na lógica; rápido | Emely |
| Unitário - diálogo | Estados, pendência, seleção, cancelamento, sessão | Não | Em cada mudança de contexto | Emely |
| Unitário - serviço | Mapeamento de parâmetros, parse, normalização, HTTP errors, cache/limite se houver | Não | Em cada mudança do adapter | Emely |
| Integração backend | POST /chat e composição de módulos com cliente fake | Não | Após contrato e integração | Emely; fixture de Miguel |
| Aceitação T01-T24 | Comportamento do sistema como um todo | Controlada por padrão | Marco de avaliação e regressão final | Miguel consolida; todos revisam |
| UI manual/componente | UI M00, mensagens, loading, seleção, erro e acessibilidade básica | Backend local/mock | Após alteração visual e na versão final | Millena |
| Smoke live opcional | Conexão mínima e esquema da Open Library | Sim, poucas consultas deliberadas | Após adapter ou antes da demo | Miguel sondagem; Emely implementação |
| Instalação/reprodução | README, env, dados, comandos, execução limpa | Pode começar offline | Antes do pacote e release | Miguel executa; Emely corrige |
| Defesa/documentação | Pergunta inédita, falha explicada e contribuição | Demonstração controlada ou live identificada | Ensaio e apresentação | Todos |

### Oráculos e fronteiras de responsabilidade

Especificar oráculos localmente: interpretador retorna intenção, score, margem e decisão; extrator retorna entidade tipada; diálogo retorna pergunta/seleção/consulta; adapter converte resposta externa em modelo interno; UI mostra estado. Se o comportamento falhar, essa separação ajuda a localizar causa sem atribuir automaticamente todo erro à IA.

**Mocks:** use resposta controlada para vazio, múltiplos resultados e campos ausentes. **Live:** uma chamada real pode comprovar conectividade naquela hora, mas não é estável nem mede accuracy. Anote horário, consulta, fonte e status. Não misture resultado ao vivo no valor de referência sem validar o dado.

### Ambientes separados

1) Fixtures determinísticas para a suite; 2) backend integrado offline; 3) smoke de API externa em baixa frequência; 4) demo ao vivo ou demonstração controlada claramente identificada. Evite depender da Open Library para completar cada execução de CI/teste.

## 4. Catálogo de testes automatizados por componente

Esta tabela amplia o plano de 24 perguntas com os testes internos que sustentam as funcionalidades. IDs NLP, ENT, DIA, API, RES, UI, E2E, DATA, MET, RUN e REG identificam famílias. A prioridade “MVP” marca comportamento coberto antes da entrega; P1/condicional depende de a melhoria entrar no código.

### Normalização

| ID | Comportamento coberto | Ação/execução | Assert principal | Prioridade |
| --- | --- | --- | --- | --- |
| NLP-01 | Texto vazio | Normalizar e interpretar | Retorna estado de entrada vazia; não consulta API. | MVP |
| NLP-02 | Caixa e espaços | Normalizar e comparar | A variação de caixa/espaço não altera indevidamente o rótulo. | MVP |
| NLP-03 | Acentos | Comparar scores | Resultado segue política documentada; original e entidade ficam preservados. | MVP |
| NLP-04 | Pontuação/aspas | Extrair entidade | Título não inclui aspas/pontuação espúria; texto original permanece disponível. | MVP |

### Representação

| ID | Comportamento coberto | Ação/execução | Assert principal | Prioridade |
| --- | --- | --- | --- | --- |
| NLP-05 | Tfidf ajuste separado | Construir vetorizador | Vocabulário/IDF se ajustam apenas na referência; corpus de teste não é lido no fit. | MVP |
| NLP-06 | Frase fora do vocabulário | Transformar e comparar | Sem erro/crash; score baixo ou abstenção conforme política. | MVP |
| NLP-07 | Intenção prevista | Predizer frase nova conhecida por padrão | Retorna intenção, score e evidência do exemplo vizinho. | MVP |
| NLP-08 | Agregação por classe | Calcular agregado configurado | Classe e agregado correspondem à regra congelada e são reproduzíveis. | MVP |

### Decisão

| ID | Comportamento coberto | Ação/execução | Assert principal | Prioridade |
| --- | --- | --- | --- | --- |
| NLP-09 | Abaixo do limiar | Aplicar política | Abstenção/esclarecimento; não chamar fonte externa. | MVP |
| NLP-10 | Margem de ambiguidade | Aplicar política | Pergunta de esclarecimento conforme hipóteses; nenhuma consulta arbitrária. | MVP |
| NLP-11 | Aceitação pelo limiar e margem | Aplicar política | Intenção aceita; parâmetros seguem para extração. | MVP |
| NLP-12 | Fora do escopo | Aplicar política/regras explícitas | Abster-se ou encaminhar informativamente; não inventar intenção de negócio. | MVP |
| NLP-13 | Pontuação não é probabilidade | Inspecionar schema, logs e UI técnica | Campo identificado como similaridade/score; nenhum texto afirma probabilidade calibrada. | MVP |

### Entidades

| ID | Comportamento coberto | Ação/execução | Assert principal | Prioridade |
| --- | --- | --- | --- | --- |
| ENT-01 | Busca por título | Extrair parâmetros | title correto, sem palavras do comando. | MVP |
| ENT-02 | Busca por autor | Extrair parâmetros | author preserva nome composto completo. | MVP |
| ENT-03 | Busca por assunto | Extrair parâmetros | subject correto; “sobre” não perdido antes da extração. | MVP |
| ENT-04 | Título versus autor | Extrair intenção e entidade | Autor+lista vs título+campo autor; não decidir só pelo verbo “escreveu”. | MVP |
| ENT-05 | Parâmetro ausente | Executar diálogo | Pergunta pelo parâmetro; API não chamada antes da resposta. | MVP |
| ENT-06 | Entidades em conflito | Executar extração/política | Pede confirmação; não descarta informação silenciosamente. | MVP |

### Diálogo

| ID | Comportamento coberto | Ação/execução | Assert principal | Prioridade |
| --- | --- | --- | --- | --- |
| DIA-01 | Pergunta de esclarecimento | Executar novo turno | Pede nome completo/ação; não assume entidade. | MVP |
| DIA-02 | Resposta à pendência | Enviar turno seguinte | Completa intenção pendente e continua uma vez; não reclassifica fragmento como fora do escopo. | MVP |
| DIA-03 | Lista de resultados | Mostrar lista | Lista é numerada e guarda mesma ordem/IDs na sessão. | MVP |
| DIA-04 | Seleção válida | Usuário envia “o segundo” | Seleciona o segundo ID; sem nova busca por literal “segundo”. | MVP |
| DIA-05 | Seleção inválida | Usuário envia “o quarto” | Informa seleção inválida e mantém contexto recuperável. | MVP |
| DIA-06 | Detalhe da seleção | Perguntar “quem escreveu?” | Consulta/autoria do ID selecionado; não primeiro resultado. | MVP |
| DIA-07 | Sem referência ativa | Usuário pergunta “qual o ano dele?” | Pede qual obra; não inventa contexto. | MVP |
| DIA-08 | Cancelamento | Usuário cancela | Limpa pendência e não realiza consulta posterior. | MVP |
| DIA-09 | Nova busca substitui pendência | Usuário inicia busca explícita por assunto | Nova busca prevalece; não mistura parâmetros antigos. | MVP |
| DIA-10 | Isolamento de sessão | Selecionar “o segundo” em cada | IDs/contextos permanecem separados. | MVP |
| DIA-11 | Mudança de assunto | Nova busca sobre astronomia | Busca atual é astronomia; não reutiliza autor Orwell. | MVP |
| DIA-12 | Recomendação limitada | Processar solicitação | Interpreta descoberta por assunto; não afirma personalização. | MVP |

## 5. Catálogo: serviço, respostas e interface

### Serviço de livros

| ID | Comportamento coberto | Ação/execução | Assert principal | Prioridade |
| --- | --- | --- | --- | --- |
| API-01 | Consulta de título | Buscar título com parâmetros codificados | Parâmetro segue adapter; retorna IDs e títulos normalizados. | MVP |
| API-02 | Consulta de autor | Buscar obras de autor composto | Campo correto enviado; autores múltiplos preservados. | MVP |
| API-03 | Consulta por assunto | Buscar subject | Consulta coerente; resposta normalizada em lista. | MVP |
| API-04 | Detalhe por identificador | Consultar detalhe | ID pedido coincide com retorno; campos de obra vs edição identificados. | MVP |
| API-05 | JSON mínimo válido | Normalizar | Campos ausentes são opcionais; app não quebra nem inventa. | MVP |
| API-06 | Lista vazia | Consultar serviço | Estado not_found/search_empty distinto de erro HTTP. | MVP |
| API-07 | Múltiplas correspondências | Consultar e renderizar | Mantém candidatos distintos e IDs; sistema pede seleção. | MVP |
| API-08 | ISBN solicitado ausente | Pedir ISBN | Informa que a fonte não fornece o campo; não diz ISBN inexistente. | MVP |
| API-09 | Falha de rede | Consultar serviço | Erro vira estado de indisponibilidade; nenhuma resposta inventada. | MVP |
| API-10 | Timeout | Consultar com timeout configurado | Finaliza dentro do timeout; mensagem adequada; sem retentativa infinita. | MVP |
| API-11 | 429 e Retry-After | Executar política de retentativa | Respeita limite/cabeçalho com tentativas limitadas; teste usa relógio falso. | MVP |
| API-12 | Erro 5xx | Consultar | Retentativa limitada se política permitir; resposta final é fallback. | MVP |
| API-13 | JSON inválido/schema inesperado | Normalizar | Erro controlado e log sem conteúdo sensível; usuário recebe indisponibilidade. | MVP |
| API-14 | Limite e concorrência | Enviar várias requisições em sessões | Limitador evita superar política configurada; teste não espera em tempo real. | MVP |
| API-15 | Cache (se incluído P1) | Chamar adapter duas vezes | Segunda chamada reutiliza cache dentro da validade; consulta diferente não colide. | P1 opcional |
| API-16 | Contagem de requisições | Busca com etapa de detalhe | Chamadas previstas e limitadas; sem uma chamada por resultado sem controle. | MVP |
| API-17 | Parâmetro seguro/codificação | Montar requisição | Cliente usa codificação HTTP/params, não concatenação insegura de URL. | MVP |
| API-18 | Sem acesso à rede nos unitários | Executar suite unitária | Cliente fake intercepta todas as chamadas; suite funciona offline. | MVP |

### Resposta e interface

| ID | Comportamento coberto | Ação/execução | Assert principal | Prioridade |
| --- | --- | --- | --- | --- |
| RES-01 | Template título | Gerar resposta | Mostra só os campos existentes e identificação da fonte. | MVP |
| RES-02 | Template autor | Gerar resposta | Deixa claro que lista foi retornada pela fonte; não afirma completude mundial. | MVP |
| RES-03 | Template assunto | Gerar resposta | Resultado é apresentado como relacionado ao tema, não recomendação individual. | MVP |
| RES-04 | Campo opcional | Gerar card | Oculta ou informa ausência de forma limpa; demais dados aparecem. | MVP |
| RES-05 | Obra/edição e data | Gerar detalhe | Rótulos distinguem primeira publicação de ano da edição. | MVP |
| RES-06 | Proveniência | Renderizar mensagem | Link/crédito corresponde ao item exibido quando disponível. | MVP |
| UI-01 | Enviar mensagem | Enviar pergunta válida | Mensagem aparece uma vez e resposta chega com estado correto. | MVP |
| UI-02 | Entrada vazia | Enviar vazio/só espaços | Validação clara; sem chamada ao backend/API. | MVP |
| UI-03 | Carregamento e erro | Enviar mensagem | Estado de carregamento termina; erro não deixa chat travado. | MVP |
| UI-04 | Renderização de múltiplos resultados | Abrir resultados | Todos IDs/títulos selecionáveis, sem trocar a ordem. | MVP |
| UI-05 | Seleção do usuário | Selecionar item e pedir detalhe | UI envia referência estável conforme contrato. | MVP |
| UI-06 | Falha da fonte na UI | Enviar nova busca | Exibe mensagem de fonte indisponível e mantém uso básico. | MVP |
| UI-07 | Sem resultado na UI | Enviar consulta | Diferencia ausência de resultado de indisponibilidade. | MVP |
| UI-08 | Acessibilidade/usabilidade básica | Navegar teclado, foco e contraste básico | Campo/envio/resultados operáveis; foco visível e rótulos compreensíveis. | MVP |
| UI-09 | Modo técnico, se implementado P1 | Abrir modo de demonstração | Scores chamados similaridade; ausência não quebra chat regular. | P1 opcional |

**Sobre limites da Open Library:** limite compartilhado requer teste de concorrência usando relógio/transport fake. Não inferir rate limit após enviar carga real. A suíte default não deve exigir chave; conferir que nenhum segredo está embutido. Smoke live fica manual, com poucas chamadas e conforme as regras atuais da fonte.

## 6. Catálogo: ponta a ponta, dados, métricas e entrega

### Sistema, dados e defesa

| ID | Comportamento coberto | Ação/execução | Assert principal | Prioridade |
| --- | --- | --- | --- | --- |
| E2E-01 | Busca por título completa | “Procure Dom Casmurro” | Interpreta título, consulta, normaliza e mostra resposta/fonte. | MVP |
| E2E-02 | Busca por autor completa | “Quais livros Machado de Assis escreveu?” | Lista de obras do autor; sem tratar como biografia. | MVP |
| E2E-03 | Busca por assunto completa | “Mostre ficção científica” | Consulta tema e exibe resultados. | MVP |
| E2E-04 | Detalhes completos | “Quem escreveu Dom Casmurro?” | Encontra obra, apresenta campo existente e origem. | MVP |
| E2E-05 | Dados necessários ausentes | “Busque um livro” | Pergunta título; API não chamada antes de completar. | MVP |
| E2E-06 | Pergunta ambígua | “Machado” | Pede esclarecimento; próxima resposta continua a tarefa. | MVP |
| E2E-07 | Fora do escopo | “Qual a previsão do tempo?” | Abstenção adequada sem chamar Open Library. | MVP |
| E2E-08 | Múltiplos itens e continuação | Busca → “o segundo” → “quem escreveu?” | Detalhe corresponde à seleção da conversa. | MVP |
| E2E-09 | API indisponível integrada | Busca por título | UI recebe fallback e contexto fica consistente. | MVP |
| E2E-10 | Usuário troca de demanda | Nova busca por astronomia | Contexto anterior não contamina nova intenção. | MVP |
| DATA-01 | Grupos de paráfrase | Auditar grupo_variacao | Nenhum grupo aparece em dois splits. | MVP |
| DATA-02 | Duplicata exata | Comparar normalizados e IDs | Duplicata relatada/revisada; identificadores únicos. | MVP |
| DATA-03 | Balanceamento e classe rara | Contar classes por split | Divergência relatada; sem classe de teste omitida silenciosamente. | MVP |
| MET-01 | Métricas com resposta conhecida | Calcular relatório e confusão | Contagens e denominadores coincidem com cálculo manual. | MVP |
| MET-02 | Taxa de fallback | Calcular separadamente | Total e tipos de fallback aparecem, não somente porcentagem agregada. | MVP |
| RUN-01 | Instalação README limpa | Instalar e executar os passos | Servidor, índice, UI e testes básicos sobem sem arquivo secreto. | MVP |
| RUN-02 | Configuração sem credencial privada | Inicializar MVP | Open Library pública funciona conforme política sem key hardcoded. | MVP |
| REG-01 | Regressão dos erros analisados | Reexecutar após correção | Erro corrigido fica coberto e versão/conjunto atualizado. | MVP |
| DOC-01 | Histórico de resultados | Revisar entrega | Todo resultado inclui versão e modo controlado/ao vivo; nenhum caso não rodado marcado passou. | MVP |

**DEF-01 - Pergunta inédita; DEF-02 - Explicação individual.** São verificações de ensaio/autoria, não assertions automatizadas. O professor pode introduzir formulação nova; a equipe demonstra resposta, esclarece ou aponta limite e correção. O objetivo não é prometer que qualquer frase inédita será interpretada corretamente.

## 7. Suite de aceitação de 24 perguntas - T01 a T12

**Exigência oficial:** pelo menos 20 casos com esperado, obtido e resultado. Os 24 seguintes dão margem mínima e cobrem reformulação, ambiguidade, ausência, fora de domínio e diálogo. São casos planejados, ainda sem resultado obtido. Definir parâmetros e fontes controladas antes de rodar.

| ID e entrada | Intenção esperada | Comportamento esperado |
| --- | --- | --- |
| T01<br>Procure Dom Casmurro | buscar_por_titulo | Com fixture determinística, consulta título e lista candidatos. |
| T02<br>Você encontra o livro A Hora da Estrela? | buscar_por_titulo | Extrai título sem comando e apresenta resultados/fonte. |
| T03<br>Estou atrás de um livro chamado 1984 | buscar_por_titulo | Reformulação; aceita se passar política congelada, senão registra falha/abstenção. |
| T04<br>Procure Dom Casmuro | buscar_por_titulo | Pequeno typo; consulta candidata ou pede confirmação, nunca inventa match. |
| T05<br>Quais livros Machado de Assis escreveu? | buscar_obras_autor | Consulta por autor e apresenta lista. |
| T06<br>Mostre obras de Clarice Lispector | buscar_obras_autor | Preserva autor composto completo. |
| T07<br>Quero ler algo escrito por George Orwell | buscar_obras_autor | Reformulação; avaliar reconhecido ou abstenção conforme split, sem alterar depois. |
| T08<br>Quero livros sobre inteligência artificial | buscar_por_assunto | Extrai assunto e consulta categoria/subject. |
| T09<br>Me mostre ficção científica | buscar_por_assunto | Interpreta gênero e retorna obras controladas. |
| T10<br>Alguma leitura a respeito de astronomia? | buscar_por_assunto | Paráfrase de assunto; avaliar interpretação definida. |
| T11<br>Quem escreveu Dom Casmurro? | consultar_detalhes | Resolve título, mostra autor se campo disponível e indica fonte. |
| T12<br>Quero saber mais sobre A Hora da Estrela | consultar_detalhes | Mostra detalhes do item identificado ou pede seleção. |

## 8. Suite de aceitação - T13 a T24

| ID e entrada | Intenção/estado esperado | Comportamento esperado |
| --- | --- | --- |
| T13<br>Livros de história | Assunto ou esclarecimento | Política congelada antes da execução; não escolher esperado após ver saída. |
| T14<br>Machado | Esclarecimento | Pede nome completo/confirma hipótese; não assume qual pessoa ou ação. |
| T15<br>Busque um livro | buscar_por_titulo, incompleta | Pergunta o título e não chama a API antes do parâmetro. |
| T16<br>Mostre livros de um autor | buscar_obras_autor, incompleta | Pergunta quem é o autor. |
| T17<br>Qual a previsão do tempo? | Fora do escopo | Abstenção simples; não consulta API de livros. |
| T18<br>Renove meu empréstimo | Operação fora do escopo | Explica que CAPITU não opera empréstimos; orienta biblioteca. |
| T19<br>Procure Zyx Livro 8472 | buscar_por_titulo | Retorno vazio controlado: “não encontrei nesta fonte”; não afirmar inexistência. |
| T20<br>Obras de Zyx Autor 8472 | buscar_obras_autor | Retorno vazio controlado e pedido de revisão do nome. |
| T21<br>Procure 1984 | buscar_por_titulo | Timeout injetado: mensagem de indisponibilidade, sem crash. |
| T22<br>Procure Dom Casmurro | buscar_por_titulo | Vários resultados controlados; numera e pede seleção. |
| T23<br>Busca → “o segundo” → “quem escreveu?” | Seleção + consultar_detalhes | Seleciona ID 2 e responde para a obra escolhida. |
| T24<br>Busca por Orwell → nova busca sobre astronomia | buscar_por_assunto | Nova demanda substitui contexto de autor. |

**Para executar:** adicionar Resultado obtido, Passou?, versão, data e modo. Registre score/parâmetros para diagnóstico. T19/T20 usam fake vazio para estabilidade. T21 não causa timeout ao vivo. T13 recebe oráculo aprovado pelo grupo antes da execução. Os 24 casos atendem ao mínimo como plano; só contam como evidência após preenchimento real.

## 9. Dataset, generalização e prevenção de vazamento

| Verificação | Regra e evidência |
| --- | --- |
| Origem | Identificar autorais, coleta consentida/simulada e versões; não chamar exemplos sintéticos de pesquisa com público |
| Guia de rótulos | Definir intenção, entidade e casos difíceis antes da coleta |
| Grupos de variação | Manter paráfrases próximas, templates e derivados no mesmo grupo de split |
| Ajuste do vetorizador | fit/fit_transform somente referência/treino; validação/teste usam transform |
| Seleção de limiar | Usar validação; escolher após congelar teste; registrar configuração |
| Duplicatas | Auditar ID, texto normalizado e grupos relacionados entre arquivos |
| Balanceamento | Contar exemplos/classe em cada split e destacar classe pequena |
| Entidades inéditas | Exercitar nomes de autor/títulos que não são somente os exemplos mais repetidos |
| Correção pós-teste | Usar falhas do teste para melhoria transforma o conjunto; repetir nova avaliação independente |
| Artefatos | Guardar hash/versão de corpus, split, biblioteca, configuração e commit associado |

### Split recomendado pelo plano

Referência/treino 60%, validação 20%, teste 20% por grupo de formulação, estratificado quando o volume permitir. Para aproximadamente 120 frases e quatro classes, alguns grupos terão poucos casos: reportar contagem por intenção; não inferir precisão estatística ampla. Divisão aleatória linha a linha pode vazar paráfrases.

No motor por similaridade, frases de referência funcionam como exemplos rotulados consultados. Ajustar IDF também é etapa de preparação. Não descrever essa implementação como classificador supervisionado treinado se não houver regressão logística/Naive Bayes/etc.

## 10. Métricas, denominadores e critérios de análise

| Medida | Definição para o projeto | O que não esquecer |
| --- | --- | --- |
| Taxa de sucesso funcional | Casos cujo comportamento completo foi correto ÷ casos executados | Pode contar fallback correto como sucesso; definir oráculo por caso. |
| Accuracy de intenção | Intenções corretas ÷ entradas com rótulo único | Ambíguos ficam em avaliação de diálogo, ou têm conjunto de rótulos válido definido. |
| Precision por intenção | TP/(TP+FP) | Baixa precision indica consultas naquela intenção disparadas indevidamente. |
| Recall por intenção | TP/(TP+FN) | Baixo recall indica mensagens daquela intenção perdidas/abstidas. |
| F1 e macro-F1 | Média harmônica P/R e média das classes | Macro mostra classe fraca mesmo quando uma classe domina. |
| Matriz de confusão | Contagens real × previsto, com rejeição explicitada | Não esconder classe “abstenção” nem contar ambiguous como qualquer coisa. |
| Taxa de fallback | Fallbacks ÷ entradas; ainda separar adequados e inadequados | Taxa baixa pode ocultar falsa aceitação; taxa alta pode mostrar baixa utilidade. |
| Acerto de entidades | Entidades corretas ÷ entidades avaliadas | Calcular separadamente da intenção. |
| Taxa de erro externo | Respostas de erro/falha ÷ consultas externas simuladas | Fixtures medem tratamento; não estima uptime real. |
| Latência, opcional | Tempo por fase e ponta a ponta | Separar API externa de processamento local; descrever amostra. |

### Matriz do erro por camadas

Para cada falha, localizar uma ou mais etapas: intenção → entidade → estado/contexto → query/HTTP → normalização → resposta/UI. Guardar input, esperado/obtido, scores, estado prévio, fixture/status, causa provável, impacto, ação e teste de regressão.

**Exigência:** analisar no mínimo três falhas observadas. Não selecionar somente casos simulados de API sem falhas reais do sistema. Se os 24 casos não renderem três erros, ampliar com paráfrases e entradas difíceis, registrar descobertas e não fabricar dados.

## 11. API externa, fixtures e smoke tests

- **Fixture JSON:** guardar respostas pequenas reduzidas às chaves necessárias, IDs inventados/claramente controlados e origem declarada.

- **Testar consulta do adapter:** método, endpoint, query parameters e codificação, em vez de afirmar dependência exata da ordenação viva.

- **Testar respostas:** lista válida, múltiplos candidatos, vazio, autor múltiplo, campo ausente, obra/edição, JSON inválido e erro HTTP.

- **Mock de rede:** bloquear chamada real no conjunto padrão; falhar teste explicitamente se uma requisição externa escapar do fixture.

- **Rate limiter:** usar relógio falso e requisições concorrentes simuladas; teste não aguarda intervalos reais nem gera rajada ao vivo.

- **Smoke opcional:** uma consulta deliberada por rota/recorte, anotada com hora, query, status e esquema mínimo; manter baixa frequência e consultar política Open Library atual.

- **Separar fato:** fonte fora do ar é falha externa daquele momento; retorno vazio não prova que a obra inexiste; campos opcionais ausentes não são erro do classificador.

- **Proveniência:** resultado exibido aponta fonte quando disponível e nunca afirma disponibilidade no acervo universitário.

A Open Library documenta política de consultas e recomenda limitar/cuidar de uso. Antes da execução, Miguel registra política vigente em G04 e Emely codifica limite compartilhado em E10. Não fixar em teste uma expectativa temporal do serviço sem verificar a documentação atual.

## 12. Interface, estados de diálogo e apresentação

| Sequência manual | Passos | Verificação |
| --- | --- | --- |
| UI-01 | Abrir CAPITU local; enviar mensagem válida | Mensagem e resposta única, ordem legível, sem bloqueio |
| UI-02 | Enviar vazio/só espaços | Aviso; nenhuma busca desnecessária |
| UI-03 | Fazer backend atrasar/falhar | Indicador para e erro pode ser recuperado |
| UI-04 | Mostrar lista controlada com três itens | IDs/títulos e ordem visíveis; seleção possível |
| UI-05 | Selecionar item e pedir detalhe | Request referencia resultado selecionado |
| UI-06 | API simulada como indisponível | Usuário entende que fonte falhou; estado não fica preso |
| UI-07 | API controlada sem resultado | Mensagem difere de indisponibilidade |
| UI-08 | Navegar por teclado/foco/labels | Controles operáveis e mensagens compreensíveis |
| UI-09 | Ativar modo técnico, se implementado | Score é explicitado como similaridade; UI comum continua funcional |

**UI existente:** Millena já construiu a interface conforme informado. M00 guarda autoria; M02 registra/ajusta compatibilidade com contrato; M03 integra; M05/M08 validam. Os casos de interface não exigem reconstrução total nem cobram de Millena o núcleo de PLN.

### Desafio de defesa

Treinar formulação que não esteja no corpus: alguém pede “algo parecido com 1984” ou combina autor e tema. Registrar a pergunta antes, mostrar a decisão real, aceitar esclarecimento/abstenção como comportamento defensável e explicar qual mudança em dados/regra/teste faria. Não adicionar a pergunta ao corpus e reportá-la como inédita na mesma avaliação.

## 13. Rotina da equipe e critérios de conclusão

| Responsável | Pacote de trabalho de testes | Quando/entrega |
| --- | --- | --- |
| Emely | NLP/ENT/DIA/API/E2E/MET/REG; mock padrão; métricas; três falhas | Automação e integração até 12/11; diagnóstico até 15/11 |
| Millena | UI-01 a UI-09, roteiros, screenshots e PDF visual; preserva UI original | Fluxos locais, integração e revisão até 24/11 |
| Miguel | G03 fixtures, G04 smoke/sondagem, T01-T24, RUN-01, evidências | Tabela consolidada até 12/11; instalação até 16/11 |
| Todos | Revisão cruzada e ensaio inédito; autoria e limites | Ensaio de equipe em 22/11; versão final 24/11 |

### Checklist por task

☐ A especificação tem entrada e estado definidos antes da execução?

☐ Há resultado esperado verificável, inclusive efeitos colaterais de API/contexto?

☐ A execução registra versão, fixture/modo, obtido e passou/falhou/bloqueado?

☐ Uma falha leva ao componente provável e vira regressão após correção?

☐ Dados, logs e evidências não contêm credenciais ou dados pessoais?

☐ O integrante responsável consegue explicar por que a verificação é adequada?

### Ordem até a entrega

**Até 12/10:** contrato/backend mínimo; **20/10:** corpus/similaridade inicial; **31/10:** entidades/contexto; **06/11:** quatro intenções integradas; **12/11:** congelamento funcional, executar coleta principal; **17/11:** falhas e reprodução; **21/11:** relatório/pacote candidatos; **22/11:** ensaio; **23-24/11:** apenas bloqueadores, regressão, congelamento e backup; **25/11:** entrega.

## 14. O que deve constar na tabela final de resultados

| Coluna | Exemplo de conteúdo esperado |
| --- | --- |
| ID | T11 |
| Entrada / sequência | “Quem escreveu Dom Casmurro?” |
| Estado inicial | Sessão limpa; versão v1.0.0; fixture search-dom-casmurro.json |
| Intenção/entidade esperadas | consultar_detalhes; title=Dom Casmurro; field=author |
| Comportamento esperado | Resultado com autor, se campo retornado, e origem; não inventar dado |
| Obtido | Transcrição curta ou referência a log, IDs e mensagem |
| Passou? | Sim / Não / Bloqueado / Não executado; critério se falhou |
| Scores e estado | Score/margem, decisão e IDs selecionados quando útil |
| Modo / versão | pytest mock, backend controlado, UI manual ou smoke live; commit/dataset |
| Evidência | Caminho de saída, fixture ou screenshot sem segredo |

**Registros não feitos:** antes da execução, Resultado obtido fica vazio ou “Não executado”; nunca preencher como passou com resposta estimada. Após execução, preservar falhas originais; versão corrigida gera outra linha/execução.

### Exemplo estrutural sem resultado inventado

| ID | Esperado | Obtido | Situação |
| --- | --- | --- | --- |
| T21 | timeout simulado produz indisponibilidade; sem crash | A preencher na execução | Não executado |

A tabela da A3 pode ser uma planilha ou CSV; este documento define os campos e o catálogo. Atualizar os casos diretos para usar os mesmos IDs T01-T24 do planejamento CAPITU para manter rastreabilidade.

## 15. Critérios de aceite do conjunto de testes

| Gate | Condição para marcar concluído |
| --- | --- |
| GATE-A Planejamento | T01-T24 têm pré-condições/oráculos congelados e cobrem mínimo oficial. |
| GATE-B Corpus | Splits/grupos sem vazamento conhecido; fit só no treino; contagens por classe guardadas. |
| GATE-C Unitários | Lógica de decisão, contexto e adapter testada com casos normais, borda e erro. |
| GATE-D Integração | Quatro fluxos E2E usando API controlada; consulta é coerente com intenção/parâmetro. |
| GATE-E Resiliência | Vazio, campo ausente, múltiplos resultados, rede/timeout/429/5xx e JSON inválido têm saída definida. |
| GATE-F UI | Mensagens, lista/seleção, loading, erros e sessão verificados manualmente na UI existente. |
| GATE-G Métricas | Resultados reproduzíveis; taxa de sucesso, métricas de classe/confusão e fallback têm denominadores. |
| GATE-H Falhas | Pelo menos três falhas reais examinadas; causa e melhoria fundamentadas. |
| GATE-I Entrega | README funciona em ambiente novo; release/pacote e tabela de evidências conferidos. |
| GATE-J Defesa | Os três integrantes conseguem explicar mecanismo, teste, contribuição e limite. |

Um gate que falhe não deve ser ocultado. Registrar o que bloqueia, quem resolve e data; a ausência de teste executado não equivale a aprovado. Resultados e meta interna devem ser reportados mesmo se abaixo de 85%.

## 16. Referências e relação com documentos existentes

### Enunciado oficial

A3_Projeto_Chatbots_IA_40_pontos_20260923193204(2).docx, entregue pela equipe: R1-R7; etapas; relatório; testes; critérios.

### Aula complementar

Aula_A3_Tecnologias_Chatbots_IA_Detalhada071020261_20261007160815.pdf, 23 páginas, Professor Marcelo da Silva: intenções/contexto; TF-IDF; treino/teste; fallback; métricas; defesa.

### Planejamento do grupo

CAPITU_Planejamento_Detalhado_Equipe.pdf: escopo aprovado, quatro intents, entidades, API, 24 casos-base, limites e métricas.

### Plano de tarefas

CAPITU_Plano_Tarefas_Equipe_Entrega_25_11_2026.pdf: E/M/G tasks, dependências, entrega, fixtures, T01-T24 e papéis de validação.

### scikit-learn: text features

[https://scikit-learn.org/stable/modules/feature_extraction.html#text-feature-extraction](https://scikit-learn.org/stable/modules/feature_extraction.html#text-feature-extraction)

### scikit-learn: metrics

[https://scikit-learn.org/stable/modules/model_evaluation.html#classification-metrics](https://scikit-learn.org/stable/modules/model_evaluation.html#classification-metrics)

### scikit-learn: common pitfalls

[https://scikit-learn.org/stable/common_pitfalls.html](https://scikit-learn.org/stable/common_pitfalls.html)

### Open Library APIs / guidelines

[https://openlibrary.org/developers/api](https://openlibrary.org/developers/api)

### Open Library Search API

[https://openlibrary.org/dev/docs/api/search](https://openlibrary.org/dev/docs/api/search)

### Open Library Books API

[https://openlibrary.org/dev/docs/api/books](https://openlibrary.org/dev/docs/api/books)

### FastAPI testing

[https://fastapi.tiangolo.com/tutorial/testing/](https://fastapi.tiangolo.com/tutorial/testing/)

### HTTPX timeouts

[https://www.python-httpx.org/advanced/timeouts/](https://www.python-httpx.org/advanced/timeouts/)

### pytest fixtures

[https://docs.pytest.org/en/stable/how-to/fixtures.html](https://docs.pytest.org/en/stable/how-to/fixtures.html)

**Proveniência:** os planos e cenários estão alinhados ao escopo declarado e à aprovação relatada pelo grupo. O código e os testes ainda devem ser desenvolvidos e executados. Documentação online pode mudar; reconferir durante a implementação. Esta documentação foi redigida com apoio de IA generativa e precisa de revisão pela equipe antes de ser entregue como parte do projeto.
