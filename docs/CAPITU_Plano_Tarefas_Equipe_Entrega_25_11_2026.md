# Plano de tarefas da equipe CAPITU até 25 de novembro de 2026

> **Sincronização obrigatória: qualquer alteração neste documento deve ser reproduzida no PDF e no Markdown do mesmo nome-base antes do commit.**
> **PDF correspondente:** `CAPITU_Plano_Tarefas_Equipe_Entrega_25_11_2026.pdf`

## Plano de execução e divisão de tarefas

**Equipe:** Emely, Millena e Miguel<br>**Professor:** Marcelo da Silva<br>**Entrega:** 25 de novembro de 2026<br>**Planejamento:** 7 de outubro a 25 de novembro de 2026 • Versão 1.0

**Estado informado pela equipe:** proposta de implementação aprovada pelo professor; UI já desenvolvida por Millena. A UI é contribuição concluída declarada, ainda não inspecionada nesta etapa. Este plano agenda integração, validação e ajustes sem atribuir novamente a criação da interface.

Emely assume arquitetura, PLN, diálogo, API, integração, métricas e revisão técnica, com mais tarefas e maior complexidade. Millena e Miguel recebem oito tarefas restantes cada, com 32 horas estimadas por pessoa e atividades delimitadas de menor complexidade.

| Pessoa | Tasks restantes | Horas estimadas | Responsabilidade principal |
| --- | --- | --- | --- |
| Emely | 18 | 88 | Núcleo técnico e coordenação |
| Millena | 8 | 32 | UI existente, dados e materiais |
| Miguel | 8 | 32 | Dados, testes guiados e reprodução |

**Carga total restante:** 152 horas-pessoa. A igualdade entre Millena e Miguel considera apenas o trabalho futuro. O tempo já gasto na UI não foi informado e não é contado como zero; deve ser registrado separadamente.

**Premissa de disponibilidade:** reservar cerca de 14 h/semana para Emely e 5 h/semana para Millena e Miguel, incluindo folga. Estimativas não são compromissos garantidos: revisar na primeira reunião. Duração em horas representa esforço; a janela de datas representa tempo corrido para executar e revisar.

**Escopo mantido:** Python; TF-IDF + similaridade e regras; Open Library; chat web local; quatro intenções bibliográficas. Sem LLM, personalização, empréstimos ou disponibilidade do acervo universitário.

**Legenda:** exigências da A3 são os requisitos obrigatórios; divisão, horas, datas internas, ferramentas e testes propostos são decisões/recomendações de planejamento. Todos devem entender o fluxo geral e explicar uma contribuição verificável.

## 1. Calendário e marcos internos

| Janela | Emely | Millena | Miguel |
| --- | --- | --- | --- |
| 07-13/10 | E01-E02: contratos e base | M01; início M02 | G01-G02: dados/negativos |
| 14-20/10 | E03-E04: corpus e similaridade | M02: UI documentada | Preparar estudo das fixtures |
| 21-27/10 | E05; início E06 | M04: texto do relatório | G03; início G04 |
| 28/10-03/11 | Final E06; E07-E08 | Revisar UI contra contrato | Final G04; preparar casos |
| 04-10/11 | E09-E10; início E11 | M03; início M05 | G05; início G06 |
| 11-17/11 | Final E11; E12-E13 | Final M05; revisar textos | Final G06; G07 |
| 18-21/11 | E14-E15: relatório/pacote | M06-M07 | G08: evidências/defesa |
| 22-24/11 | E16-E18: ensaio/reserva/freeze | M08: revisão e ensaio | Participar do ensaio e revisar sua fala |
| 25/11 | Submissão recomendada à Emely | Disponível para apoio | Disponível para apoio |

| Data-alvo | Marco e condição de saída |
| --- | --- |
| 12/10 | Backend mínimo e contrato disponíveis; UI pode usar dados simulados |
| 20/10 | Interpretador TF-IDF inicial funcionando; corpus separado |
| 31/10 | Entidades e contexto funcionando |
| 06/11 | Quatro intenções integradas com serviço de livros |
| 12/11 | Congelamento de funcionalidades; avaliação e logs coletados |
| 17/11 | Falhas analisadas e instalação revisada |
| 21/11 | Relatório e pacote candidatos prontos |
| 22/11 | Ensaio de toda a equipe |
| 23/11 | Reserva para bloqueadores, sem novas funcionalidades |
| 24/11 | Congelamento final e backup |
| 25/11 | Entrega no canal e horário oficiais a confirmar |

As datas acima são marcos internos, não datas informadas pelo professor, exceto a entrega de 25/11 indicada pela equipe. Encontros/horários dos ensaios serão combinados. Não depender de desenvolvimento no próprio dia da entrega. Se a submissão ocorrer antes do horário habitual, antecipar a checagem de E18.

## 2. Dependências e acordos de trabalho

**Caminho crítico:** E01 → E02 + dados M01/G01/G02 → E03 → E04 → E05 → E06 → E07; em paralelo G03/G04 preparam E08. E07 + E08 → E09 → E10 → E11 → E12 → E13 → E14 → M06 → E15 → ensaio/revisão → E18 → entrega.

**Handoff essencial:** Emely entrega contrato e exemplos em 09/10; Millena/Miguel entregam dados até 13/10; Miguel entrega sondagem até 30/10; Emely entrega backend integrado até 06/11; os dois validam até 12/11. Texto técnico vai à Millena até 19/11; o PDF consolidado volta até 20/11.

**Trabalho paralelo:** dados das duas pessoas não exigem backend; UI usa simulador antes da API; fixtures e sondagem não exigem cliente completo; relatório avança por seções durante desenvolvimento. Conflitos de contrato e regras de IA ficam com Emely, sem deixar Millena/Miguel responsáveis por arquitetura.

### Rotina de acompanhamento

Reunião curta semanal, em horário a combinar: verificar task concluída, evidência, bloqueio e próxima entrega. Quem detectar bloqueio comunica à equipe em até um dia; dependente não marca task como concluída sem receber o artefato. Emely acompanha o caminho crítico e revisa contribuições técnicas leves dos colegas.

### Critério comum de conclusão

Uma task termina quando: entrega existe; aceite foi conferido; teste/validação foi executado; resultado e versão foram registrados; dependente recebeu o artefato; responsável consegue explicar o que fez. Registrar em docs/evidence/ID ou estrutura equivalente, com commit quando houver código/dados.

### Como interpretar os testes de cada task

Código de IA, backend e API exige testes automatizados significativos com pytest e respostas controladas. UI, coleta, relatório e slides usam roteiros manuais ou revisão documental: não criar testes artificiais para checar uma frase do texto. Em todos os casos registrar entrada/procedimento, esperado, obtido e resultado. Millena/Miguel podem usar templates fornecidos por Emely para automação simples.

### Trabalho já concluído pela Millena

**M00 • UI inicial • status: concluída conforme informação da equipe.** Preservar autoria e histórico. Tempo e data reais: a registrar; não estimados retroativamente. Evidência: código, commits e screenshots originais. Validação futura: M02 verifica fluxos e compatibilidade; M03 integra; M05/M08 avaliam. A UI não deve ser reconstruída sem necessidade técnica identificada.

### Reserva e redução de escopo

P0: quatro intenções, corpus, PLN, contexto mínimo, API, falhas, 20+ testes, métricas, três erros, execução, relatório e defesa. P1 condicionado: cache simples/mode técnico útil. Adiar ISBN, capas, filtros e qualquer recomendação. Se cronograma atrasar, cortar melhorias visuais e cache avançado; preservar limites de chamadas e tratamento de falhas. A sobrecarga de Emely é deliberada, mas exige monitoramento; revisão operacional dos colegas pode liberar tempo sem transferir IA complexa.

## 3. Tasks de Emely

18 tarefas restantes • 88 horas estimadas • Esta página: E01 e E02

### E01 • Arquitetura executável e contratos

**Responsável:** Emely • **Esforço:** 3 h • **Janela:** 07/10 a 09/10/2026<br>**Complexidade:** Alta • **Dependências:** nenhuma<br>**Prioridade:** P0; incrementos citados só se couberem • **Rastreabilidade:** B09-B10; R1-R4

**Descrição e o que fazer:** Definir módulos, endpoint do chat e modelos de mensagem, interpretação, livro e sessão; fixar precedência e limites. Preparar contrato que permita UI e testes trabalharem antes da API real.

**O que consultar:** Planejamento aprovado; FastAPI/Pydantic para schemas; requisitos R1-R4; estrutura real da UI da Millena.

**Teste ou validação a escrever/executar:** Escrever cenários de contrato: mensagem válida aceita; entrada vazia tratada; resposta contém texto, estado e lista. Converter para teste automatizado quando E02 existir.

**Aceite e evidência:** Contrato versionado, diagrama e exemplos de payload revisados por Millena e Miguel.

### E02 • Ambiente, backend mínimo e infraestrutura de teste

**Responsável:** Emely • **Esforço:** 4 h • **Janela:** 10/10 a 12/10/2026<br>**Complexidade:** Média/alta • **Dependências:** E01<br>**Prioridade:** P0; incrementos citados só se couberem • **Rastreabilidade:** B11-B12; R1, R4, R7

**Descrição e o que fazer:** Criar ambiente Python, dependências, endpoint mínimo e dados simulados; organizar pytest, configurações e inicialização. Entregar base executável sem IA fingida.

**O que consultar:** FastAPI: testes e execução; pytest: fixtures; contratos E01; Git/README.

**Teste ou validação a escrever/executar:** Escrever teste de POST /chat com payload válido e inválido; verificar estado HTTP e schema. Rodar instalação em ambiente virtual novo.

**Aceite e evidência:** Servidor local e suite inicial executam; Miguel e Millena conseguem usar contrato. Registrar comandos.

## 3. Tasks de Emely

18 tarefas restantes • 88 horas estimadas • Esta página: E03 e E04

### E03 • Curadoria, exemplos complementares e split sem vazamento

**Responsável:** Emely • **Esforço:** 4 h • **Janela:** 14/10 a 16/10/2026<br>**Complexidade:** Alta • **Dependências:** M01, G01, G02<br>**Prioridade:** P0; incrementos citados só se couberem • **Rastreabilidade:** B05-B08; R2-R3, R5-R6

**Descrição e o que fazer:** Revisar 80 frases coletadas, adicionar cerca de 40 diversas, resolver rótulos, agrupar paráfrases e separar referência/validação/teste. Registrar origem e exemplos negativos.

**O que consultar:** Guia de anotação; exemplos de Millena/Miguel; scikit-learn: pitfalls e separação; material da aula.

**Teste ou validação a escrever/executar:** Escrever teste de auditoria que acusa ID/texto duplicado e grupo presente em mais de um split; revisar equilíbrio por classe e entidades não vistas.

**Aceite e evidência:** Corpus inicial de cerca de 120 frases, splits e manifesto; teste final não usado no ajuste. Quantidade é meta, não mínimo oficial.

### E04 • TF-IDF, cosseno e pontuação de intenção

**Responsável:** Emely • **Esforço:** 7 h • **Janela:** 17/10 a 20/10/2026<br>**Complexidade:** Alta • **Dependências:** E02, E03<br>**Prioridade:** P0; incrementos citados só se couberem • **Rastreabilidade:** B13-B14; R3-R4

**Descrição e o que fazer:** Implementar normalização, ajuste TF-IDF somente na referência, transformação de novas mensagens, cosseno e agregação por intenção; salvar artefatos e configuração.

**O que consultar:** scikit-learn: TfidfVectorizer/cosine_similarity; aula págs. 9-12; split E03.

**Teste ou validação a escrever/executar:** Escrever testes de frase inédita, ausência de vocabulário e ajuste sem dados de teste; conferir intenção em casos simples e score rastreável. Não testar somente frases decoradas.

**Aceite e evidência:** Interpretador retorna candidatos e scores reproduzíveis; script constrói índice sem consultar teste final.

## 3. Tasks de Emely

18 tarefas restantes • 88 horas estimadas • Esta página: E05 e E06

### E05 • Limiar, ambiguidade e rejeição

**Responsável:** Emely • **Esforço:** 6 h • **Janela:** 21/10 a 24/10/2026<br>**Complexidade:** Alta • **Dependências:** E04, G02<br>**Prioridade:** P0; incrementos citados só se couberem • **Rastreabilidade:** B15; R3-R4, R6

**Descrição e o que fazer:** Comparar vizinho mais próximo e agregação na validação; selecionar limiar e margem. Implementar aceitação, esclarecimento e abstenção; tratar pedidos operacionais conhecidos.

**O que consultar:** Dados negativos/ambíguos G02; documentação de similaridade; aula pág. 15. O exemplo 0,70 não é valor obrigatório.

**Teste ou validação a escrever/executar:** Escrever testes abaixo do limiar, empate entre intenções, texto sem evidência e fora do domínio; avaliar falso aceite e fallback desnecessário na validação.

**Aceite e evidência:** Política e parâmetros congelados antes do teste; justificativa registrada. Score não é rotulado como probabilidade.

### E06 • Extração de entidades e informação faltante

**Responsável:** Emely • **Esforço:** 6 h • **Janela:** 25/10 a 28/10/2026<br>**Complexidade:** Alta • **Dependências:** E04, E05<br>**Prioridade:** P0; incrementos citados só se couberem • **Rastreabilidade:** B16; R4

**Descrição e o que fazer:** Extrair título, autor, assunto e campo solicitado com regras; preservar texto original. Identificar parâmetro ausente e conflito; ISBN fica opcional fora da rota crítica.

**O que consultar:** Python re/Unicode; guia de intenções; padrões e exemplos curados; modelo de mensagem E01.

**Teste ou validação a escrever/executar:** Escrever testes “livros de Machado” versus “quem escreveu Dom Casmurro”, título entre aspas, nome composto e parâmetro ausente; conferir entidade além do rótulo.

**Aceite e evidência:** Parâmetros corretos ou esclarecimento explícito; regras documentadas sem remover palavras discriminativas.

## 3. Tasks de Emely

18 tarefas restantes • 88 horas estimadas • Esta página: E07 e E08

### E07 • Contexto mínimo e máquina de estados

**Responsável:** Emely • **Esforço:** 5 h • **Janela:** 29/10 a 31/10/2026<br>**Complexidade:** Alta • **Dependências:** E05, E06<br>**Prioridade:** P0; incrementos citados só se couberem • **Rastreabilidade:** B17; R1, R4

**Descrição e o que fazer:** Implementar intenção pendente, pergunta por parâmetro, lista e obra selecionada; seleção numérica, cancelamento e nova demanda. Separar sessões para não compartilhar contexto.

**O que consultar:** Contrato E01; requisitos R1/R4; exemplos da aula pág. 6; casos de Miguel.

**Teste ou validação a escrever/executar:** Escrever testes de busca → “o segundo” → autoria; parâmetro pendente → resposta curta; nova busca limpa estado; duas sessões não se contaminam.

**Aceite e evidência:** Diálogos completos previsíveis; transições e critérios de esclarecimento versionados.

### E08 • Cliente Open Library e normalização

**Responsável:** Emely • **Esforço:** 6 h • **Janela:** 01/11 a 03/11/2026<br>**Complexidade:** Alta • **Dependências:** E02, G03, G04<br>**Prioridade:** P0; incrementos citados só se couberem • **Rastreabilidade:** B18-B19; R4

**Descrição e o que fazer:** Implementar busca por título/autor/assunto e detalhe por ID. Normalizar obra/edição, autores, datas, descrição e fonte; tratar campos opcionais.

**O que consultar:** Open Library: Search API, Books API, diretrizes; fixtures G03 e sondagem G04; httpx.

**Teste ou validação a escrever/executar:** Escrever testes com respostas controladas de cada rota, campos ausentes, edição/obra e autor múltiplo; validar parâmetros enviados sem depender da ordem ao vivo.

**Aceite e evidência:** Cliente real e modo controlado isolados; IDs preservados; não atribuir estoque institucional nem inventar campo.

## 3. Tasks de Emely

18 tarefas restantes • 88 horas estimadas • Esta página: E09 e E10

### E09 • Integração completa e respostas bibliográficas

**Responsável:** Emely • **Esforço:** 7 h • **Janela:** 04/11 a 06/11/2026<br>**Complexidade:** Alta • **Dependências:** E07, E08<br>**Prioridade:** P0; incrementos citados só se couberem • **Rastreabilidade:** B21; R1-R4

**Descrição e o que fazer:** Conectar endpoint, interpretação, política, diálogo e fonte. Gerar templates das quatro intenções; retornar estado e candidatos para UI existente.

**O que consultar:** Contratos E01; UI documentada M02; componentes E04-E08; critérios T01-T24.

**Teste ou validação a escrever/executar:** Escrever quatro testes ponta a ponta com API simulada, cobrindo intenção, entidade, consulta e resposta/fonte. Incluir pedido de parâmetro e seleção.

**Aceite e evidência:** Quatro intenções funcionam no backend; Millena consegue integrar UI sem alterar contrato informalmente.

### E10 • Robustez HTTP e controle de chamadas

**Responsável:** Emely • **Esforço:** 5 h • **Janela:** 07/11 a 09/11/2026<br>**Complexidade:** Alta • **Dependências:** E09<br>**Prioridade:** P0; incrementos citados só se couberem • **Rastreabilidade:** B20, B23; R4

**Descrição e o que fazer:** Tratar timeout, rede, 429/5xx, JSON inválido e vazio; limitar chamadas entre sessões, retentar quando apropriado, respeitar Retry-After e adicionar cache simples se couber.

**O que consultar:** httpx: exceções/timeouts; Open Library: limites vigentes; RFC/documentação de Retry-After; política do projeto.

**Teste ou validação a escrever/executar:** Escrever testes com timeout, 429, 503, JSON inválido, resultado vazio e chamadas repetidas. Verificar limite e quantidade de retentativas usando cliente controlado, sem sobrecarregar fonte.

**Aceite e evidência:** Falhas viram resposta útil; sem loop de retentativa. Registrar política e redução de chamadas.

## 3. Tasks de Emely

18 tarefas restantes • 88 horas estimadas • Esta página: E11 e E12

### E11 • Avaliação de PLN, métricas e rastreamento

**Responsável:** Emely • **Esforço:** 6 h • **Janela:** 10/11 a 12/11/2026<br>**Complexidade:** Alta • **Dependências:** E09, E10, G05, M03<br>**Prioridade:** P0; incrementos citados só se couberem • **Rastreabilidade:** B24, B28-B29; R3, R5-R6

**Descrição e o que fazer:** Executar conjunto de intenção congelado; produzir accuracy, precision/recall/F1, matriz, fallback e acerto de parâmetros. Expor modo técnico e separar sucesso do diálogo.

**O que consultar:** scikit-learn: classification_report/confusion_matrix; plano de testes; versões de corpus; aula págs. 18-19.

**Teste ou validação a escrever/executar:** Escrever teste do cálculo com pequeno conjunto cujo resultado manual é conhecido, incluindo erro e abstenção. Conferir denominadores e não excluir rejeições silenciosamente.

**Aceite e evidência:** Resultados reais reproduzíveis, logs sem dados sensíveis e diagnóstico por classe; congelamento funcional em 12/11.

### E12 • Diagnóstico técnico de pelo menos três falhas

**Responsável:** Emely • **Esforço:** 5 h • **Janela:** 13/11 a 15/11/2026<br>**Complexidade:** Alta • **Dependências:** E11, G06, M05<br>**Prioridade:** P0; incrementos citados só se couberem • **Rastreabilidade:** B30-B31; R5-R6 / Marco 5

**Descrição e o que fazer:** Selecionar erros reais, rastrear causa em PLN, parâmetros ou estado, propor correções prioritárias. Se necessário, ampliar perguntas difíceis; não fabricar falhas.

**O que consultar:** Resultados de Emely/Miguel/Millena; scores, matriz e logs; guia de rótulos.

**Teste ou validação a escrever/executar:** Escrever caso de regressão para cada falha corrigida. Quando usar teste final para melhorar, registrar isso e avaliar correção em novas formulações independentes.

**Aceite e evidência:** Três fichas com esperado/obtido, causa, impacto e ação; comparação honesta das versões.

## 3. Tasks de Emely

18 tarefas restantes • 88 horas estimadas • Esta página: E13 e E14

### E13 • Revisão técnica do README e reprodução

**Responsável:** Emely • **Esforço:** 4 h • **Janela:** 16/11 a 17/11/2026<br>**Complexidade:** Média/alta • **Dependências:** E12, G07<br>**Prioridade:** P0; incrementos citados só se couberem • **Rastreabilidade:** B32; R7

**Descrição e o que fazer:** Corrigir problemas apontados na instalação independente; validar dependências, scripts, artefatos e comandos de teste. Remover segredo e caminho específico da máquina.

**O que consultar:** README G07; resultado da instalação de Miguel; configuração Python/FastAPI/pytest.

**Teste ou validação a escrever/executar:** Reexecutar instalação e chat em ambiente novo usando apenas README; executar teste de smoke com fixture e busca ao vivo limitada quando disponível.

**Aceite e evidência:** Execução reproduzível e pré-requisitos explícitos; evidência do ambiente e comandos.

### E14 • Seções técnicas do relatório

**Responsável:** Emely • **Esforço:** 5 h • **Janela:** 18/11 a 19/11/2026<br>**Complexidade:** Alta • **Dependências:** E12, E13<br>**Prioridade:** P0; incrementos citados só se couberem • **Rastreabilidade:** B33; relatório 4, IA 8, testes 6

**Descrição e o que fazer:** Redigir arquitetura/IA, implementação e avaliação: algoritmo, alternativa, limiar, versões, trechos autorais curtos, métricas e três falhas. Entregar texto à Millena para consolidar.

**O que consultar:** Enunciado: seções 4-6; material da aula; código e experimentos reais; referências oficiais.

**Teste ou validação a escrever/executar:** Fazer validação documental: conferir toda métrica contra arquivo de resultados e todos os diagramas contra o código. Colega aponta afirmações não sustentadas.

**Aceite e evidência:** Seções 4-6 completas, com evidência e limites; sem resultado inventado nem confiança tratada como probabilidade.

## 3. Tasks de Emely

18 tarefas restantes • 88 horas estimadas • Esta página: E15 e E16

### E15 • Revisão de autoria e pacote executável

**Responsável:** Emely • **Esforço:** 4 h • **Janela:** 20/11 a 21/11/2026<br>**Complexidade:** Alta • **Dependências:** E14, M06, G07<br>**Prioridade:** P0; incrementos citados só se couberem • **Rastreabilidade:** B33-B34; R7 / entrega

**Descrição e o que fazer:** Revisar relatório consolidado, README, dados e código; produzir release/ZIP executável. Verificar rastreabilidade, seis páginas efetivas, referências, IA generativa e contribuições.

**O que consultar:** Checklist oficial; versões finais dos integrantes; licença/permissão dos dados; histórico de contribuição.

**Teste ou validação a escrever/executar:** Validar pacote extraído em pasta nova; executar comandos de instalação/testes; procurar senhas/chaves e arquivos privados. Conferir checklist de entrega item a item.

**Aceite e evidência:** Candidato final pronto em 21/11; relatório e pacote coerentes, sem credenciais privadas.

### E16 • Defesa do algoritmo e coordenação do ensaio

**Responsável:** Emely • **Esforço:** 4 h • **Janela:** 22/11 a 22/11/2026<br>**Complexidade:** Média/alta • **Dependências:** E15, M07, G08<br>**Prioridade:** P0; incrementos citados só se couberem • **Rastreabilidade:** B35-B36; defesa 3 / autoria

**Descrição e o que fazer:** Preparar demonstração do pipeline, scores, parâmetros e um erro. Distribuir falas técnicas; conduzir ensaio completo e perguntas reformuladas.

**O que consultar:** Roteiro de slides; material pág. 20; código real; resultado e matriz; tempo oficial a confirmar.

**Teste ou validação a escrever/executar:** Validar três perguntas inéditas em ensaio e explicar tecnicamente eventual falha. Cronometrar apresentação e conferir que todos explicam sua contribuição e fluxo geral.

**Aceite e evidência:** Roteiro ajustado; perguntas e respostas do ensaio registradas; todos participam.

## 3. Tasks de Emely

18 tarefas restantes • 88 horas estimadas • Esta página: E17 e E18

### E17 • Reserva técnica e correções finais

**Responsável:** Emely • **Esforço:** 4 h • **Janela:** 23/11 a 23/11/2026<br>**Complexidade:** Alta • **Dependências:** E16<br>**Prioridade:** P0; incrementos citados só se couberem • **Rastreabilidade:** B31, B37; R4-R7

**Descrição e o que fazer:** Usar reserva para erros bloqueadores do ensaio; evitar funcionalidade nova. Revisar mudanças com os dois colegas e regenerar resultados/documentos afetados.

**O que consultar:** Lista de defeitos do ensaio; logs; testes de regressão; checklist do pacote.

**Teste ou validação a escrever/executar:** Escrever/regressar teste que reproduz cada bloqueador corrigido; rodar suite pertinente. Se não houver defeito, usar horas para revisão de riscos e defesa.

**Aceite e evidência:** Sem bloqueador conhecido; qualquer alteração tem evidência e versão atualizada.

### E18 • Congelamento final e organização da entrega

**Responsável:** Emely • **Esforço:** 3 h • **Janela:** 24/11 a 24/11/2026<br>**Complexidade:** Média/alta • **Dependências:** E17, M08<br>**Prioridade:** P0; incrementos citados só se couberem • **Rastreabilidade:** B34; R7 / entrega final

**Descrição e o que fazer:** Congelar release, conferir PDF/ZIP/repositório, acesso do professor e backup. Preparar checklist para submissão em 25/11; registrar versão sem prometer envio automático.

**O que consultar:** Plataforma/canal oficial e horário de entrega a confirmar; checklist R1-R7; pacote validado.

**Teste ou validação a escrever/executar:** Abrir todos os arquivos finais, executar smoke do pacote congelado, verificar acesso ao repositório/links em sessão apropriada e confirmar conteúdo do ZIP.

**Aceite e evidência:** Arquivos e backup prontos em 24/11. Responsável recomendado pela submissão: Emely; comprovante em 25/11.

## 4. Tasks de Millena

8 tarefas restantes • 32 horas estimadas • Esta página: M01 e M02

### M01 • Coletar exemplos e organizar casos de uso

**Responsável:** Millena • **Esforço:** 4 h • **Janela:** 08/10 a 13/10/2026<br>**Complexidade:** Baixa • **Dependências:** nenhuma<br>**Prioridade:** P0; incrementos citados só se couberem • **Rastreabilidade:** B01-B02, B06; R2

**Descrição e o que fazer:** Criar 40 frases diversas, dez por intenção; marcar entidades e origem. Documentar fluxos do usuário e limites aprovados; não gerar só troca de título.

**O que consultar:** Quatro intenções do planejamento; guia inicial alinhado com Emely; dez perguntas do Marco 1.

**Teste ou validação a escrever/executar:** Validação manual em dupla com Miguel: classificar amostra sem olhar rótulo, marcar divergências e duplicatas; preencher exemplos de esperado sem alegar resposta real.

**Aceite e evidência:** 40 frases revisáveis entregues a Emely com origem e grupos aproximados; tabela de casos de uso.

### M02 • Registrar UI existente e validar fluxos básicos

**Responsável:** Millena • **Esforço:** 4 h • **Janela:** 14/10 a 20/10/2026<br>**Complexidade:** Baixa • **Dependências:** E01, E02<br>**Prioridade:** P0; incrementos citados só se couberem • **Rastreabilidade:** B22 parcial; R1 / autoria

**Descrição e o que fazer:** Preservar UI já criada; documentar componentes e ajustar somente o necessário para payload, carregamento, mensagem vazia e exibição de resultado. Usar backend simulado.

**O que consultar:** Código da própria UI; contrato E01; endpoint E02; princípios básicos de mensagens de estado.

**Teste ou validação a escrever/executar:** Escrever roteiro UI-01 a UI-04: envio válido, entrada vazia, carregamento e lista simulada. Executar manualmente; teste de documentação/fluxo não precisa automatização artificial.

**Aceite e evidência:** UI original registrada com evidência de autoria; ajustes pequenos funcionando contra simulador.

## 4. Tasks de Millena

8 tarefas restantes • 32 horas estimadas • Esta página: M03 e M04

### M03 • Ligar UI ao endpoint integrado

**Responsável:** Millena • **Esforço:** 4 h • **Janela:** 07/11 a 09/11/2026<br>**Complexidade:** Baixa, com contrato pronto • **Dependências:** E09, M02<br>**Prioridade:** P0; incrementos citados só se couberem • **Rastreabilidade:** B22; R1-R4

**Descrição e o que fazer:** Configurar URL local e fetch/envio; renderizar mensagens e lista; enviar seleção pelo contrato. Emely resolve lógica/erros de backend; não transferir arquitetura para Millena.

**O que consultar:** Contrato E01; exemplos reais de E09; MDN fetch; guia da UI existente.

**Teste ou validação a escrever/executar:** Escrever e executar UI-05 a UI-08: título, autor, assunto e detalhes, contra API controlada; verificar corpo enviado e resposta apresentada.

**Aceite e evidência:** Quatro fluxos acessíveis na UI; screenshots e divergências registrados, sem criar regras de IA no frontend.

### M04 • Redigir problema, requisitos e discussão inicial

**Responsável:** Millena • **Esforço:** 4 h • **Janela:** 21/10 a 27/10/2026<br>**Complexidade:** Baixa • **Dependências:** M01, M02<br>**Prioridade:** P0; incrementos citados só se couberem • **Rastreabilidade:** B33 parcial; relatório

**Descrição e o que fazer:** Preparar seções 1, 2 e rascunho da 7: problema, público, objetivos, escopo, intenções, fluxos e limitações. Atualizar discussão após resultados.

**O que consultar:** Enunciado: seções obrigatórias; proposta aprovada; decisões e casos de uso; documentação da UI.

**Teste ou validação a escrever/executar:** Validação documental por checklist: cenário simulado identificado, quatro intenções consistentes, nenhum acervo/resultado alegado sem evidência; revisão por Miguel.

**Aceite e evidência:** Texto editável com fontes e limites, pronto para consolidação; não contar screenshots como conteúdo principal.

## 4. Tasks de Millena

8 tarefas restantes • 32 horas estimadas • Esta página: M05 e M06

### M05 • Testar usabilidade e estados de erro na UI

**Responsável:** Millena • **Esforço:** 4 h • **Janela:** 10/11 a 12/11/2026<br>**Complexidade:** Baixa • **Dependências:** M03, E10<br>**Prioridade:** P0; incrementos citados só se couberem • **Rastreabilidade:** B28 parcial; R1, R5

**Descrição e o que fazer:** Executar testes de seleção, parâmetro ausente, falha externa, retorno vazio e troca de contexto; registrar obtido e screenshots com versão. Não corrigir backend complexo.

**O que consultar:** Plano de 24 casos; endpoint E10; fixtures de Miguel; estados e limites da aplicação.

**Teste ou validação a escrever/executar:** Escrever UI-09 a UI-14 com pré-condição e esperado; executar manualmente com respostas controladas e verificar que mensagem não fica presa no carregamento.

**Aceite e evidência:** Seis casos de interface documentados; defeitos encaminhados a Emely com passos para reproduzir.

### M06 • Consolidar e formatar relatório final

**Responsável:** Millena • **Esforço:** 4 h • **Janela:** 20/11 a 20/11/2026<br>**Complexidade:** Baixa • **Dependências:** M04, G02, E14<br>**Prioridade:** P0; incrementos citados só se couberem • **Rastreabilidade:** B33; relatório 4

**Descrição e o que fazer:** Unir textos das três pessoas, identificar integrantes/turma, organizar figuras e tabelas, referências e contribuições; exportar PDF. Emely valida conteúdo técnico.

**O que consultar:** Seções M04, dados G02, texto E14; enunciado de seis páginas efetivas e formato sugerido.

**Teste ou validação a escrever/executar:** Validar PDF visualmente página a página; checklist de seções, legibilidade, referências e seis páginas efetivas excluindo capa/anexos; revisar contra textos de origem.

**Aceite e evidência:** PDF candidato e fonte editável sem corte/duplicação; autoria e IA generativa declaradas.

## 4. Tasks de Millena

8 tarefas restantes • 32 horas estimadas • Esta página: M07 e M08

### M07 • Montar slides e fala da interface

**Responsável:** Millena • **Esforço:** 4 h • **Janela:** 21/11 a 21/11/2026<br>**Complexidade:** Baixa • **Dependências:** M06, E14<br>**Prioridade:** P0; incrementos citados só se couberem • **Rastreabilidade:** B35-B36; defesa

**Descrição e o que fazer:** Preparar slides simples com problema, intenções, diagrama, demonstração, métricas reais e limites; usar dados fornecidos por Emely. Preparar fala sobre UI e coleta.

**O que consultar:** Relatório consolidado; diagrama; material da aula pág. 20; resultados de E11/E12.

**Teste ou validação a escrever/executar:** Validação de apresentação: abrir slides, conferir números contra relatório, executar percurso visual e cronometrar sua fala; confirmar exemplo inédito sem alegar acerto garantido.

**Aceite e evidência:** Slides prontos para ensaio de 22/11; contribuição pessoal e limites explicáveis.

### M08 • Revisão visual final e ensaio individual

**Responsável:** Millena • **Esforço:** 4 h • **Janela:** 23/11 a 24/11/2026<br>**Complexidade:** Baixa • **Dependências:** M07, E16<br>**Prioridade:** P0; incrementos citados só se couberem • **Rastreabilidade:** B35-B37; R1 / autoria / defesa

**Descrição e o que fazer:** Aplicar ajustes visuais do ensaio, revisar links/fontes/screenshots e arquivos finais; preparar explicação da UI, casos de uso e limites. Guardar evidências da contribuição já realizada.

**O que consultar:** Registro do ensaio; checklist de entrega; PDF/slides/UI congelados; histórico de commits.

**Teste ou validação a escrever/executar:** Reexecutar roteiro manual das quatro intenções na versão final; abrir PDF/slides em outro visualizador e responder duas perguntas sobre sua contribuição.

**Aceite e evidência:** Aprovação visual registrada e materiais enviados a Emely antes do congelamento de 24/11.

## 5. Tasks de Miguel

8 tarefas restantes • 32 horas estimadas • Esta página: G01 e G02

### G01 • Coletar exemplos independentes

**Responsável:** Miguel • **Esforço:** 4 h • **Janela:** 08/10 a 13/10/2026<br>**Complexidade:** Baixa • **Dependências:** nenhuma<br>**Prioridade:** P0; incrementos citados só se couberem • **Rastreabilidade:** B06-B07; R2

**Descrição e o que fazer:** Criar 40 frases, dez por intenção, com estruturas distintas das de Millena; anotar parâmetros e origem. Revisar rótulos cruzados sem copiar padrões.

**O que consultar:** Guia das intenções; proposta; orientações de dados da aula pág. 7; material de Millena para detectar duplicatas.

**Teste ou validação a escrever/executar:** Validação manual em dupla: rotular amostra sem rótulo visível, identificar frases ambíguas e grupos similares. Corrigir divergência documentada.

**Aceite e evidência:** 40 exemplos e relatório de revisão entregues para E03; nenhuma pergunta pessoal sensível.

### G02 • Casos negativos e ficha dos dados

**Responsável:** Miguel • **Esforço:** 4 h • **Janela:** 08/10 a 13/10/2026<br>**Complexidade:** Baixa • **Dependências:** G01 parcial<br>**Prioridade:** P0; incrementos citados só se couberem • **Rastreabilidade:** B05, B07, B33 parcial; R2-R6

**Descrição e o que fazer:** Preparar cerca de 12 entradas fora do escopo e oito ambíguas em arquivo separado. Redigir origem, formato, privacidade, autorização e guia inicial de anotação com Emely.

**O que consultar:** Limites do projeto; aula págs. 7/15/18; direitos e documentação dos dados externos.

**Teste ou validação a escrever/executar:** Validação por checklist: negativos não são perguntas válidas apenas mal escritas; ambiguidade não é forçada a classe; revisar pelo menos uma frase de cada tipo com Emely.

**Aceite e evidência:** Conjunto negativo/ambíguo e seção 3 dos dados prontos; atualizar após curadoria E03.

## 5. Tasks de Miguel

8 tarefas restantes • 32 horas estimadas • Esta página: G03 e G04

### G03 • Preparar respostas controladas da API

**Responsável:** Miguel • **Esforço:** 4 h • **Janela:** 21/10 a 25/10/2026<br>**Complexidade:** Baixa • **Dependências:** E01, E02<br>**Prioridade:** P0; incrementos citados só se couberem • **Rastreabilidade:** B27 parcial; R4-R5

**Descrição e o que fazer:** Criar pequenos JSONs autorizados ou fictícios para livro único, vários, vazio, campos ausentes e edição. Usar fixture/template fornecido por Emely; não construir cliente HTTP.

**O que consultar:** Modelo de livro E01; Open Library: exemplos de schema; pytest fixtures; instruções de E02.

**Teste ou validação a escrever/executar:** Escrever teste simples que carrega JSON e verifica IDs, campos esperados e formato; revisar correspondência com caso de teste. Simulações devem ser identificadas.

**Aceite e evidência:** Fixtures legíveis e versionadas, prontas para E08 e testes, com origem/mode controlado.

### G04 • Sondar cobertura e documentar a Open Library

**Responsável:** Miguel • **Esforço:** 4 h • **Janela:** 26/10 a 30/10/2026<br>**Complexidade:** Baixa • **Dependências:** G03<br>**Prioridade:** P0; incrementos citados só se couberem • **Rastreabilidade:** B04; dados / API

**Descrição e o que fazer:** Executar manualmente 10-15 consultas representativas, com intervalo e sem coleta em massa. Registrar título/autor/assunto, resposta, idioma, fonte, campos e limites.

**O que consultar:** Documentação oficial Search API e diretrizes; consultas do público; condições de licenciamento. Não usar sites de terceiros como fonte técnica principal.

**Teste ou validação a escrever/executar:** Escrever roteiro API-01 a API-05: título, autor, assunto, detalhe e campo ausente; registrar resultados reais e distinguir cobertura de falha da aplicação.

**Aceite e evidência:** Ficha da API e amostra de cobertura entregues para E08; não prometer disponibilidade em português universal.

## 5. Tasks de Miguel

8 tarefas restantes • 32 horas estimadas • Esta página: G05 e G06

### G05 • Preparar e executar tabela dos 24 casos

**Responsável:** Miguel • **Esforço:** 4 h • **Janela:** 04/11 a 09/11/2026<br>**Complexidade:** Baixa, execução guiada • **Dependências:** E09 parcial, G03<br>**Prioridade:** P0; incrementos citados só se couberem • **Rastreabilidade:** B27-B28; R5

**Descrição e o que fazer:** Preparar de 04 a 06/11 os casos T01-T24 com estado inicial, esperado, intenção e modo; executar de 07 a 09/11 após E09. Caso indisponível fica pendente, não passa.

**O que consultar:** Plano anterior; contrato; README E02; fixtures G03; execução de Emely.

**Teste ou validação a escrever/executar:** Registrar teste manual de cada cenário com resultado obtido, passou/falhou e versão. Escrever três casos simples em pytest usando template de E02; Emely revisa automação.

**Aceite e evidência:** 24 registros planejados/obtidos; completar cenários de robustez após E10; dados disponíveis para E11.

### G06 • Reexecutar casos e reunir evidência de falhas

**Responsável:** Miguel • **Esforço:** 4 h • **Janela:** 10/11 a 12/11/2026<br>**Complexidade:** Baixa • **Dependências:** G05, E10<br>**Prioridade:** P0; incrementos citados só se couberem • **Rastreabilidade:** B28-B30 parcial; R5-R6

**Descrição e o que fazer:** Completar/reexecutar casos após robustez; marcar falhas e passos de reprodução. Organizar esperado/obtido/versão e lista para análise de Emely; não diagnosticar sozinho o modelo.

**O que consultar:** Logs e casos G05; interface; instruções E10; tabela de avaliação.

**Teste ou validação a escrever/executar:** Escrever roteiro de reprodução para pelo menos três erros encontrados; se faltarem, propor perguntas novas difíceis. Repetir caso para verificar consistência e não inventar erro.

**Aceite e evidência:** Tabela completa e evidências prontas para E12; modos ao vivo/controlado separados.

## 5. Tasks de Miguel

8 tarefas restantes • 32 horas estimadas • Esta página: G07 e G08

### G07 • README e instalação independente

**Responsável:** Miguel • **Esforço:** 4 h • **Janela:** 13/11 a 16/11/2026<br>**Complexidade:** Baixa, com comandos fornecidos • **Dependências:** E11, G06<br>**Prioridade:** P0; incrementos citados só se couberem • **Rastreabilidade:** B32; R7

**Descrição e o que fazer:** Organizar pré-requisitos e comandos de Emely, exemplos de execução/teste, recriação dos dados e limitações. Testar em ambiente virtual limpo e registrar problemas.

**O que consultar:** Configuração E02/E11; documentação Python venv/pytest; pacote e dataset; requisito R7.

**Teste ou validação a escrever/executar:** Escrever checklist RUN-01: instalar, construir índice, iniciar, abrir chat e rodar testes. Executar sem ajuda extra e registrar erro/passagem de cada etapa.

**Aceite e evidência:** README e log de reprodução; bloqueadores enviados a Emely antes de E13.

### G08 • Evidências individuais e contingência da defesa

**Responsável:** Miguel • **Esforço:** 4 h • **Janela:** 18/11 a 21/11/2026<br>**Complexidade:** Baixa • **Dependências:** G07, G06<br>**Prioridade:** P0; incrementos citados só se couberem • **Rastreabilidade:** B33, B36-B37; autoria / defesa

**Descrição e o que fazer:** Organizar commits/tarefas/testes dos três integrantes e suas fontes; preparar roteiro com dados controlados se internet falhar. Redigir fala sobre dados, API e testes; enviar contribuições até 19/11.

**O que consultar:** Histórico Git; resultados; fixtures; exigência de autoria e material de defesa; README.

**Teste ou validação a escrever/executar:** Executar demo sem rede usando modo controlado definido por Emely; conferir identificação desse modo. Revisar atribuição de tarefas com cada pessoa e responder duas perguntas de sua área.

**Aceite e evidência:** Quadro de contribuições para relatório/slide, backup e roteiro de contingência prontos até 21/11.

## 6. Plano de validação e entregáveis finais

**Não confundir:** as validações de cada task sustentam o trabalho, mas não eliminam a exigência de uma tabela consolidada com pelo menos 20 perguntas de teste. O plano prevê T01-T24, mais avaliações de UI/API e corpus independente do motor.

| Responsável | Parte da avaliação | Evidência |
| --- | --- | --- |
| Emely | Intenção, extração, estado, HTTP e métricas | pytest, scores, matriz e análise das três falhas |
| Millena | Interface e sequência percebida pelo usuário | Roteiros UI-01 a UI-14, screenshots e resultados |
| Miguel | Consolidação T01-T24, simulações e instalação | Tabela esperado/obtido, fixtures e log RUN-01 |
| Todos | Pergunta inédita e autoria | Ensaio, demonstração e histórico de contribuição |

Tabela consolidada: ID \| Entrada \| Estado inicial \| Intenção esperada \| Comportamento esperado \| Obtido \| Passou? \| Versão \| Modo controlado/ao vivo. Para a classificação, usar somente casos de rótulo único; para ambiguidades, medir a decisão de esclarecer. Similaridade não é probabilidade. Timeout e 429 devem ser simulados; não causar carga indevida na fonte.

### Critérios objetivos para a entrega

- Quatro intenções de negócio e base construída/curada pela equipe; fluxo completo demonstrável.

- Código executável com mecanismo de IA/PLN identificável, dados autorizados e README verificado.

- Pelo menos 20 perguntas documentadas, métricas com denominadores e três falhas reais analisadas.

- Relatório PDF/DOCX com seis páginas efetivas do texto principal, seções oficiais, identificação, referências, declaração de IA generativa e contribuições.

- Repositório acessível ou ZIP sem senhas/tokens/chaves; dados ou instruções claras de recriação.

- Slides, demo ao vivo, contingência explicitamente controlada e participação dos três integrantes.

- Arquivos finalizados em 24/11; envio em 25/11 com comprovante, no canal/horário a confirmar.

### Métricas e meta interna

Taxa geral de sucesso é a métrica central; accuracy, precision/recall/F1 e matriz avaliam intenção; fallback distingue abstenção correta e desnecessária. Meta inicial de 85% não é exigência oficial nem resultado já obtido. Se não atingida, relatar valor real, causas e limitações, sem maquiar dados.

## 7. Decisões práticas e riscos do cronograma

| Pendente | Quem encaminha e até quando |
| --- | --- |
| Disponibilidade semanal | Todos na primeira reunião; comparar com cerca de 14 h/semana Emely e 5 h/semana por colega |
| Dados de identificação | Millena registra instituição/curso/turma em M04; conferir antes do relatório |
| Tempo real da UI já feita | Millena registra M00 com evidência; não entra nas 32 h restantes |
| Repositório e acesso do professor | Emely organiza E02/E18; todos registram autoria |
| Canal, horário e forma de entrega | Emely confirma com professor até 21/11; antecedência conforme regra oficial |
| Data da apresentação | A confirmar; ensaio interno em 22/11 permanece recomendado |
| Versões e bibliotecas | Emely fixa em E02; Python/FastAPI/scikit-learn/httpx/pytest |
| Corpus e limiares | Emely define pela validação; não usar teste final para escolher |
| Disponibilidade da Open Library | Miguel sonda G04; Emely registra limites e tratamento |

| Risco | Resposta de planejamento |
| --- | --- |
| Emely é gargalo | Contrato cedo; tarefas leves paralelas; revisão semanal e corte de diferenciais |
| UI não segue contrato | M02 com simulador; M03 integra; Emely corrige contrato/backend |
| Dado atrasado ou repetitivo | Entrega conjunta em 13/10 e curadoria E03; revisão cruzada |
| Fonte sem dados/falha | Sondagem G04, erro tratado E10 e contingência G08 |
| Avaliação revela falhas | Congelar funções em 12/11; diagnóstico/correção E12 antes do pacote |
| Relatório deixado ao fim | M04 e G02 antecipam texto; E14 entrega conteúdo técnico; M06 consolida |
| Reprodução falha | G07 em ambiente limpo e E13 corrigem antes de 17/11 |
| Internet falha na defesa | Demonstração controlada identificada; não alegar consulta ao vivo |
| Mudança após release | Só bloquear/corrigir com regressão; atualizar versão, relatório e pacote |

Este plano respeita a preferência de concentrar dificuldade e volume em Emely. A igualdade dos outros dois é de oito tarefas e 32 horas restantes; não afirma igualdade do esforço histórico. A contribuição de todos continua verificável e todos participam do ensaio, mesmo sem receber task extra por reunião compartilhada.

## 8. Fontes de consulta por atividade

### Documentos do professor

Enunciado A3 de 40 pontos, DOCX fornecido; aula Tecnologias possíveis e conceitos essenciais, 23 páginas, Professor Marcelo da Silva. Requisitos R1-R7 e seções oficiais.

### Planejamento aprovado

CAPITU Planejamento detalhado para a equipe, versão 1.0; aprovação informada pela equipe. IDs B referem-se ao backlog anterior; E/M/G atribuem sua execução neste plano.

### TF-IDF e similaridade

[https://scikit-learn.org/stable/modules/feature_extraction.html#text-feature-extraction](https://scikit-learn.org/stable/modules/feature_extraction.html#text-feature-extraction)

### Métricas

[https://scikit-learn.org/stable/modules/model_evaluation.html#classification-metrics](https://scikit-learn.org/stable/modules/model_evaluation.html#classification-metrics)

### Prevenção de leakage

[https://scikit-learn.org/stable/common_pitfalls.html](https://scikit-learn.org/stable/common_pitfalls.html)

### Open Library: diretrizes e limites

[https://openlibrary.org/developers/api](https://openlibrary.org/developers/api)

### Open Library: busca

[https://openlibrary.org/dev/docs/api/search](https://openlibrary.org/dev/docs/api/search)

### Open Library: dados bibliográficos

[https://openlibrary.org/dev/docs/api/books](https://openlibrary.org/dev/docs/api/books)

### Open Library: licenciamento

[https://openlibrary.org/developers/licensing](https://openlibrary.org/developers/licensing)

### FastAPI: testes

[https://fastapi.tiangolo.com/tutorial/testing/](https://fastapi.tiangolo.com/tutorial/testing/)

### httpx: timeouts e exceções

[https://www.python-httpx.org/advanced/timeouts/](https://www.python-httpx.org/advanced/timeouts/)

### pytest: fixtures e testes

[https://docs.pytest.org/en/stable/how-to/fixtures.html](https://docs.pytest.org/en/stable/how-to/fixtures.html)

### Python: ambientes virtuais

[https://docs.python.org/3/library/venv.html](https://docs.python.org/3/library/venv.html)

### Frontend: fetch

[https://developer.mozilla.org/pt-BR/docs/Web/API/Fetch_API](https://developer.mozilla.org/pt-BR/docs/Web/API/Fetch_API)

Conferir documentação vigente na execução; links são fontes para estudo, não evidência de testes já realizados. Biblioteca é meio de implementação: a defesa deve explicar algoritmo, política e autoria. Este planejamento foi preparado com apoio de IA generativa e deve ser revisado pela equipe; resultados futuros serão registrados por quem executou.
