# Planejamento detalhado para a equipe

> **Sincronização obrigatória: qualquer alteração neste documento deve ser reproduzida no PDF e no Markdown do mesmo nome-base antes do commit.**
> **PDF correspondente:** `CAPITU_Planejamento_Detalhado_Equipe.pdf`


Chatbot inteligente de descoberta bibliográfica • Inteligência Artificial • Avaliação A3 de 40 pontos

**Destinatário:** integrantes do grupo<br>**Professor:** Marcelo da Silva<br>**Instituição, curso, turma e integrantes:** a definir<br>**Data:** 7 de outubro de 2026 • **Versão:** 1.0

**Estado do projeto:** planejamento anterior à implementação. As escolhas de cenário, escopo, limites, Python, arquitetura híbrida com TF-IDF, Open Library e chat web local foram confirmadas pela equipe nesta conversa. Protótipo, dataset, consultas experimentais e testes ainda serão desenvolvidos; não há resultados obtidos nesta versão.

**Exigência do professor:** requisito do enunciado ou orientação explícita da aula. **Decisão da equipe:** escolha confirmada. **Recomendação técnica:** proposta adicional, não exigência da avaliação. **Pendente:** item a definir ou validar.

Este documento organiza o trabalho, seus critérios de aceite e as evidências da A3. Ele não substitui o relatório técnico final: o relatório deverá descrever a implementação e os resultados reais, com pelo menos seis páginas de conteúdo efetivo.

### Roteiro de leitura

1. Enunciado e alinhamento • 2. Requisitos • 3. Problema • 4. Público • 5. Escopo • 6. Intenções • 7. Funcionalidades • 8. Alternativas de IA • 9. Arquitetura • 10. Fluxo • 11. Dados • 12. API • 13. Testes • 14. Backlog • 15. Fases e tecnologias • 16. Riscos • 17. Evidências e defesa • 18. Pendências • 19. Próximos passos.

## 1. Resumo do enunciado e alinhamento

**Exigência do professor.** Construir em equipe de 2 a 4 estudantes um chatbot para uma necessidade concreta, real ou simulada, com escopo viável, mecanismo próprio e identificável de IA/PLN, protótipo executável, avaliação e defesa técnica. Uma interface que apenas envia mensagens a uma API ou conteúdo copiado de IA generativa não atende à atividade.

| Mínimo obrigatório | Entrega planejada |
| --- | --- |
| 3 intenções/categorias | Quatro intenções bibliográficas de negócio |
| Base construída ou curada pela equipe | Corpus autoral de perguntas rotuladas, vocabulário e exemplos esperados |
| Técnica além de serviço pronto | TF-IDF + similaridade, política de decisão e regras de diálogo |
| 20 perguntas de teste | 24 casos de aceitação, mais avaliação independente do interpretador |
| 3 falhas analisadas | Erros reais com causas, impacto e melhorias |
| Relatório com 6 páginas efetivas | Seções oficiais, referências e contribuições; não confundir com este plano |
| Execução e defesa | Repositório/ZIP, README, dados, demonstração e desafio inédito |

| Critério de avaliação | Pontos |
| --- | --- |
| Problema, contexto e requisitos | 5 |
| Dados e preparação | 5 |
| Arquitetura e fundamentos de IA | 8 |
| Protótipo funcional e autoria técnica | 9 |
| Testes, resultados e reflexão crítica | 6 |
| Relatório técnico | 4 |
| Apresentação e defesa | 3 |
| TOTAL | 40 |

Arquitetura e protótipo somam 17 pontos. Não há penalidades fixas descritas: a ausência de requisitos compromete os critérios correspondentes, sem permitir calcular um desconto automático específico.

### Validação do material complementar de 23 páginas

| Referência na aula | Compatibilidade da CAPITU |
| --- | --- |
| Págs. 3, 9 e 10 | Mecanismo próprio e TF-IDF com cosseno estão contemplados; a API só fornece metadados |
| Págs. 5 e 6 | Quatro intenções, extração de parâmetros e contexto curto de seleção/esclarecimento |
| Pág. 7; págs. 11 e 12 | Corpus de referência separado de validação/teste; não avaliar apenas frases conhecidas |
| Págs. 14 e 15 | Arquitetura híbrida, precedência, abstenção, limiar e encaminhamento informativo |
| Págs. 16 e 17 | Python, scikit-learn e interface simples; escolha pela necessidade, sem LLM obrigatório |
| Págs. 18 e 19 | 24 casos planejados, métricas adequadas e análise de pelo menos três falhas reais |
| Págs. 20 e 21 | Diagrama, evidência de algoritmo, defesa de decisões e contribuição individual |
| Pág. 22 | Síntese de uma página incluída na versão do professor, com 2 frases por intenção |

**Conclusão de alinhamento:** a proposta é compatível com os dois materiais quanto à arquitetura e ao escopo. A conformidade final dependerá de implementar, preparar dados, executar testes e produzir as evidências. A aula não impõe LLM, regressão logística, banco vetorial ou limiar de 0,70: são opções/exemplos didáticos.

**Precisão conceitual:** embora a aula use a expressão “perguntas semanticamente próximas”, TF-IDF representa evidências lexicais. A equipe não deve alegar compreensão semântica geral. A preparação de vocabulário/IDF e do índice é diferente do treino de um classificador supervisionado.

## 2. Checklist e rastreabilidade dos requisitos

Os códigos R1-R7 vêm do enunciado. Os códigos C abaixo apenas identificam os demais itens para organizar a rastreabilidade. Pontos relacionados são critérios da rubrica; não são parcelas somáveis por requisito.

### C1 • Equipe e autoria

**O que significa:** 2 a 4 estudantes; cada um executa e explica contribuição verificável.<br>**Como atender:** Definir integrantes, tarefas, revisão cruzada e histórico.<br>**Evidência:** Contribuições, commits e defesa.<br>**Pontos relacionados:** Protótipo 9; defesa 3.

### C2 • Problema e Marco 1

**O que significa:** Nome, público, cenário, 3-5 problemas, objetivo, limites e 10 perguntas.<br>**Como atender:** CAPITU; cenário simulado; quatro problemas; perguntas da seção 4.<br>**Evidência:** Ficha inicial e justificativa.<br>**Pontos relacionados:** Problema 5.

### R1 • Conversação

**O que significa:** Interface utilizável e contexto quando necessário.<br>**Como atender:** Chat web local; seleção e esclarecimento na sessão.<br>**Evidência:** Demonstração e diálogos.<br>**Pontos relacionados:** Protótipo 9.

### R2 • Domínio e dados

**O que significa:** 3+ intenções, base construída/curada e limites explícitos.<br>**Como atender:** Quatro intenções, corpus próprio e escopo.<br>**Evidência:** Dataset, catálogo e README.<br>**Pontos relacionados:** Problema 5; dados 5.

### R3 • IA implementada

**O que significa:** Técnica própria além de chamar serviço.<br>**Como atender:** Pipeline TF-IDF, cosseno, agregação e política.<br>**Evidência:** Código e rastreamento da decisão.<br>**Pontos relacionados:** IA 8; protótipo 9.

### R4 • Fluxo e falhas

**O que significa:** Entrada, interpretação, consulta/decisão e resposta; abstenção.<br>**Como atender:** Arquitetura da seção 10 e exceções.<br>**Evidência:** Fluxograma e casos completos.<br>**Pontos relacionados:** IA 8; protótipo 9.

### R5 • Validação

**O que significa:** 20+ perguntas com esperado, obtido e resultado.<br>**Como atender:** 24 casos da seção 13 e corpus independente.<br>**Evidência:** Tabela executada e registros.<br>**Pontos relacionados:** Testes 6.

### R6 • Análise

**O que significa:** Taxa de acerto e métricas adequadas.<br>**Como atender:** Sucesso funcional, classificação, confusão e fallback.<br>**Evidência:** Cálculos com denominadores.<br>**Pontos relacionados:** Testes 6.

### R7 • Execução

**O que significa:** Código, instruções, dados autorizados e testes; todos explicam.<br>**Como atender:** README verificado em instalação limpa.<br>**Evidência:** Repositório/ZIP, dados e teste de instalação.<br>**Pontos relacionados:** Protótipo 9.

### C3 • Marco 2

**O que significa:** Origem, formato, licença/permissão, limpeza e exemplos de perguntas/respostas.<br>**Como atender:** Ficha de dados e versionamento.<br>**Evidência:** Guia, corpus e histórico de limpeza.<br>**Pontos relacionados:** Dados 5.

### C4 • Marco 3

**O que significa:** Arquitetura, paradigma, alternativa e fallback.<br>**Como atender:** Comparativo e política explícita.<br>**Evidência:** Diagrama e decisão arquitetural.<br>**Pontos relacionados:** IA 8.

### C5 • Marco 4

**O que significa:** Protótipo, interface, mecanismo de IA e contribuições.<br>**Como atender:** Release funcional das quatro intenções.<br>**Evidência:** Código, demo e README.<br>**Pontos relacionados:** Protótipo 9.

### C6 • Marco 5

**O que significa:** Métricas, análise de 3 falhas, melhorias, riscos e limites.<br>**Como atender:** Avaliação honesta de erros reais.<br>**Evidência:** Fichas de erro e revisão de riscos.<br>**Pontos relacionados:** Testes 6.

### C7 • Relatório

**O que significa:** 6+ páginas efetivas em PDF/DOCX, turma e integrantes; seções oficiais.<br>**Como atender:** Redigir análise técnica conforme seção 17.<br>**Evidência:** Relatório final identificado.<br>**Pontos relacionados:** Relatório 4.

### C8 • Entrega final

**O que significa:** Código acessível, README, base/recriação, testes, apresentação e demo.<br>**Como atender:** Pacote reproduzível sem senhas/tokens/chaves.<br>**Evidência:** Repositório/ZIP e materiais.<br>**Pontos relacionados:** Protótipo 9; relatório 4.

### C9 • Defesa

**O que significa:** Pergunta reformulada/mudança curta e participação de todos.<br>**Como atender:** Ensaiar explicação, falha e correção.<br>**Evidência:** Demonstração ao vivo e histórico individual.<br>**Pontos relacionados:** Defesa 3.

### C10 • Privacidade e ações

**O que significa:** Evitar dados sensíveis e alto impacto; ações externas indicadas requerem aprovação.<br>**Como atender:** Consultas bibliográficas somente leitura, dados simulados.<br>**Evidência:** Escopo e origem dos dados.<br>**Pontos relacionados:** Dados 5.

### C11 • Referências e IA generativa

**O que significa:** Declarar recursos, apoio de IA e tarefas verificáveis.<br>**Como atender:** Referências e declaração do uso realizado.<br>**Evidência:** Relatório e contribuições.<br>**Pontos relacionados:** Relatório 4; autoria 9.

### C12 • Atividade da aula, pág. 22

**O que significa:** 1 folha/slide com problema, intenções, arquitetura, justificativa e fallback.<br>**Como atender:** Primeira página da proposta breve.<br>**Evidência:** Síntese para discussão com professor.<br>**Pontos relacionados:** Sem pontuação separada informada.

**Não obrigatórios:** LLM, API paga, banco de dados, hospedagem, interface web e recomendação personalizada. O uso de API pública de livros é uma decisão/exigência deste projeto. A formatação A4, Arial/Aptos 11-12, 1,5 e margens de 2,5 cm e o tempo de oito minutos são sugestões do enunciado. Os prazos serão definidos pelo professor.

**Riscos importantes para a avaliação:** API sem PLN próprio; corpus ausente; execução quebrada; testes insuficientes; treino e teste contaminados; métricas sem registros; menos de três erros analisados; relatório sem conteúdo efetivo; integrantes sem domínio da implementação. Imagens isoladas, listagens extensas de código, capa, sumário, referências, anexos e páginas em branco não contam para as seis páginas do texto principal.

## 3. Definição do problema e objetivos

**Decisão da equipe.** Estudantes têm dificuldade para transformar títulos incompletos, nomes de autores e temas de interesse em buscas bibliográficas úteis. A CAPITU interpretará essas solicitações em português e consultará uma fonte pública, apresentando resultados identificáveis e pedindo esclarecimento quando necessário.

O cenário é uma biblioteca universitária simulada. A CAPITU é um assistente bibliográfico: não conhece a disponibilidade de exemplares da universidade. A conversa é adequada porque essas demandas podem exigir uma pergunta curta para completar parâmetros ou escolher entre resultados.

### Problemas de atendimento

- Localizar obra quando o usuário conhece parte do título.

- Descobrir obras de um autor.

- Encontrar títulos relacionados a um assunto/gênero.

- Identificar autoria e informações bibliográficas de uma obra encontrada.

### Objetivo geral

Desenvolver e avaliar um chatbot bibliográfico em português, executado localmente, que interprete solicitações de busca e consulta de obras com PLN próprio, utilize a Open Library e trate incertezas de forma explícita.

### Objetivos específicos mensuráveis

- Implementar quatro intenções e demonstrar pelo menos um diálogo completo para cada uma.

- Construir e versionar um corpus inicial recomendado de 30-40 exemplos diversos por intenção, com avaliação independente.

- Executar pelo menos 24 casos documentados, cobrindo os cenários definidos na seção 13.

- Buscar ao menos 85% de sucesso funcional na suíte congelada, registrando o resultado real mesmo que a meta não seja alcançada.

- Demonstrar tratamento de ambiguidade, retorno vazio e indisponibilidade sem inventar dados bibliográficos.

**Recomendação técnica:** tamanho do corpus e meta de 85% são metas internas iniciais, não requisitos do professor nem promessas de desempenho. A avaliação deve distinguir acerto da intenção de sucesso do diálogo.

## 4. Público-alvo e perguntas iniciais

**Público principal:** estudantes universitários que procuram obras para leitura ou estudo. **Secundário:** leitores interessados em descobrir livros por autor ou assunto. **Beneficiário institucional:** biblioteca simulada que oferece orientação bibliográfica inicial.

As dez perguntas abaixo são simuladas. Não devem ser descritas como pesquisa de campo realizada.

1. Você encontra Dom Casmurro?

2. Estou procurando A Hora da Estrela.

3. Quais livros Machado de Assis escreveu?

4. Tem obras de George Orwell?

5. Quero livros sobre inteligência artificial.

6. Mostre livros de ficção científica.

7. Quem escreveu Dom Casmurro?

8. Qual é o ano dessa edição?

9. Pode mostrar os detalhes do segundo livro?

10. Quero um livro, mas só lembro parte do título.

**Recomendação técnica:** coletar formulações espontâneas de colegas sem mostrar modelos prévios, registrar a origem e evitar dados pessoais. Essa coleta pode ampliar a diversidade; não é necessária para alegar um cenário real, pois o enunciado permite simulação documentada.

## 5. Escopo e limites

| Incluído no MVP | Fora do escopo |
| --- | --- |
| Português; busca por título, autor e assunto; detalhes | Perguntas gerais sobre qualquer assunto e biografias completas |
| Seleção de resultados e parâmetros pendentes | Memória longa, cadastro e histórico pessoal permanente |
| Fonte, dados ausentes, ambiguidades e falhas | Empréstimos, reservas, multas e acervo institucional |
| Contexto mínimo por sessão | Compras, pagamentos e ações externas operacionais |
| Descoberta por tema | Recomendação personalizada ou garantia de adequação acadêmica |
| Descrição fornecida pela fonte, quando disponível | Resumo gerado a partir da leitura integral das obras |

Títulos similares podem corresponder a obras diferentes. ISBN pertence à edição. O ano de primeira publicação não deve ser apresentado como ano de uma edição específica. “Não encontrei nesta fonte” é apropriado; a busca não prova que o livro não existe.

**Critério de sucesso de uma interação:** identificar ou esclarecer a demanda; obter parâmetros; executar consulta adequada; mostrar dados existentes; não inventar informação; tratar exceções. Uma abstenção correta pode ser sucesso funcional.

## 6. Intenções propostas e aprovadas

A equipe aprovou quatro intenções de negócio. “Fora do escopo” é um estado de rejeição e não é contado para cumprir o mínimo de três.

### buscar_por_titulo

**Objetivo:** Localizar obras pelo título.<br>**Exemplos:** “Procure Dom Casmurro”; “Você encontra A Hora da Estrela?”.<br>**Entidades:** Título; autor opcional.<br>**Ação:** Consultar título e listar candidatos.

### buscar_obras_autor

**Objetivo:** Listar obras atribuídas a um autor.<br>**Exemplos:** “Quais livros Machado de Assis escreveu?”; “Mostre obras de Clarice Lispector”.<br>**Entidades:** Autor.<br>**Ação:** Consultar obras por autor.

### buscar_por_assunto

**Objetivo:** Descobrir obras de um tema/gênero.<br>**Exemplos:** “Quero livros sobre IA”; “Mostre ficção científica”.<br>**Entidades:** Assunto/gênero.<br>**Ação:** Consultar assunto e apresentar obras.

### consultar_detalhes

**Objetivo:** Consultar obra/edição identificada.<br>**Exemplos:** “Quem escreveu Dom Casmurro?”; “Qual o ISBN do segundo?”.<br>**Entidades:** Título, ID, ISBN ou referência da sessão; campo solicitado.<br>**Ação:** Resolver obra/edição e mostrar campos disponíveis.

| Nome inicialmente cogitado | Modelagem adotada e por quê |
| --- | --- |
| buscar_livro | buscar_por_titulo: o nome anterior abrangia todas as buscas |
| buscar_autor | buscar_obras_autor: distingue catálogo de biografia do autor |
| buscar_assunto | buscar_por_assunto: ação consistente com as demais |
| detalhes_livro | consultar_detalhes: consulta de obra/edição identificada |
| recomendar_livro | Não é intenção do MVP: descoberta por tema é buscar_por_assunto; personalização amplia escopo |
| fora_do_escopo | Abstenção ou rejeição, pois não representa demanda bibliográfica |

**Distinção central:** “Quais livros foram escritos por Machado de Assis?” usa autor como parâmetro e retorna lista: buscar_obras_autor. “Quem escreveu Dom Casmurro?” usa título como parâmetro e retorna autoria: consultar_detalhes. A presença de “escreveu” não basta para decidir.

| Entrada ambígua/composta | Comportamento definido |
| --- | --- |
| Machado de Assis | Confirmar se deseja buscar obras do autor |
| Machado | Solicitar nome completo ou confirmar hipótese; não assumir pessoa |
| Dom Casmurro, sem verbo | Oferecer busca por título e confirmar se necessário |
| Livros de história | Buscar assunto se evidência suficiente; senão esclarecer |
| Recomende livros de astronomia | Descoberta por assunto, sem alegar recomendação personalizada |
| Algo parecido com 1984 | Explicar limite e solicitar assunto/gênero |
| Livros de Orwell sobre política | Esclarecer busca prioritária; filtro composto fica fora do MVP |
| Qual o ano dele? | Usar contexto apenas com uma obra identificada |

## 7. Funcionalidades e prioridade

“MVP obrigatório” abaixo significa compromisso do escopo aprovado. Não implica que cada funcionalidade isolada tenha sido exigida pelo professor.

### MVP • Interpretação

**Dados e API:** Corpus rotulado; sem API. **Técnica:** TF-IDF + similaridade.<br>**Esperado:** Intenção ou abstenção. **Fallback:** Reformular/esclarecer.

### MVP • Busca por título

**Dados e API:** Título; API. **Técnica:** PLN + extração.<br>**Esperado:** Lista numerada de candidatos. **Fallback:** Pedir título; ausência na fonte.

### MVP • Obras de autor

**Dados e API:** Autor; API. **Técnica:** PLN + extração.<br>**Esperado:** Obras atribuídas ao nome. **Fallback:** Pedir nome; homônimos.

### MVP • Busca por assunto

**Dados e API:** Assunto/gênero; API. **Técnica:** PLN + vocabulário curado.<br>**Esperado:** Obras relacionadas ao tema. **Fallback:** Pedir especificação.

### MVP • Detalhes

**Dados e API:** ID/título/contexto; API quando necessário. **Técnica:** PLN + resolução contextual.<br>**Esperado:** Campos existentes e fonte. **Fallback:** Identificar obra; campo ausente.

### MVP • Seleção e contexto

**Dados e API:** Lista, número, intenção pendente; API às vezes. **Técnica:** Regras de diálogo.<br>**Esperado:** Continuar interação coerente. **Fallback:** Número inválido; referência ausente.

### MVP • Fora do escopo

**Dados e API:** Limites e pontuações; sem API. **Técnica:** Rejeição + política.<br>**Esperado:** Explicar domínio e orientar biblioteca. **Fallback:** Abster-se sem inventar.

### MVP • Falhas externas

**Dados e API:** Erro/status; tentativa limitada. **Técnica:** Robustez, não é IA.<br>**Esperado:** Informar indisponibilidade/retorno vazio. **Fallback:** Nova tentativa voluntária.

### P1 • ISBN

**Dados e API:** Identificador; API. **Técnica:** Extração e validação.<br>**Esperado:** Identificar edição. **Fallback:** Corrigir ISBN.

### P1 • Pequenos erros de grafia

**Dados e API:** Mensagem/corpus; API após interpretação. **Técnica:** N-gramas de caracteres se justificados.<br>**Esperado:** Tolerância medida. **Fallback:** Pedir confirmação.

### P1 • Cache e rastreamento

**Dados e API:** Consulta/horário/decisão; reduz API. **Técnica:** Não é IA adicional.<br>**Esperado:** Reuso e explicação técnica. **Fallback:** Consultar novamente conforme política.

### P2 • Capas e filtros

**Dados e API:** URL/idioma/ano; API. **Técnica:** Extração para filtros.<br>**Esperado:** Melhorar identificação/refinamento. **Fallback:** Sem capa; filtro não suportado.

### P3 • Recomendação por conteúdo

**Dados e API:** Preferências e atributos; nova avaliação. **Técnica:** Ranking próprio por similaridade.<br>**Esperado:** Sugestões explicáveis. **Fallback:** Busca por assunto.

**Trade-off:** adiar personalização, filtros avançados e segunda API deixa tempo para autoria técnica, testes e relatório. P1-P3 são recomendações condicionadas ao prazo; não ampliam automaticamente o escopo aprovado.

## 8. Comparação das arquiteturas de IA

### Regras

**Funcionamento:** Palavras/condições acionam inferência. **Dificuldade:** Baixa a média.<br>**Vantagens:** Transparência e controle; execução local. **Limites:** Fragilidade a reformulação; manutenção manual.<br>**Dados:** Regras e exemplos de conflitos/exceções. **Teste e defesa:** Fácil rastrear, exige colisões e prioridades.<br>**Adequação:** Aceita com mecanismo identificável; menu estático não basta.

### TF-IDF + similaridade

**Funcionamento:** Vetores de texto comparados a perguntas rotuladas. **Dificuldade:** Baixa a média.<br>**Vantagens:** Local, simples, inspecionável e permite abstenção. **Limites:** Evidência lexical; sinônimos distantes podem falhar.<br>**Dados:** 30-40 exemplos por intenção inicialmente. **Teste e defesa:** Mostrar vizinhos e scores; testes independentes.<br>**Adequação:** Explicitamente prevista no enunciado e aula.

### Classificador supervisionado

**Funcionamento:** TF-IDF + regressão logística/Naive Bayes/SVM aprende fronteiras. **Dificuldade:** Média.<br>**Vantagens:** Combina indícios; avaliação por classe. **Limites:** Exige variedade e validação; classe prevista não resolve fora de domínio.<br>**Dados:** 40-60 por intenção para experimento inicial. **Teste e defesa:** Métricas claras; defesa um pouco mais exigente.<br>**Adequação:** Permitido; separar treino e teste.

### Híbrida

**Funcionamento:** Similaridade/classificação + regras + conhecimento externo. **Dificuldade:** Média.<br>**Vantagens:** Componentes especializados e tratamento de exceções. **Limites:** Conflitos precisam de política explícita.<br>**Dados:** Corpus de interpretação e regras contextuais. **Teste e defesa:** Boa se cada decisão for rastreável.<br>**Adequação:** Adequada; adotada na CAPITU.

### LLM + recuperação

**Funcionamento:** Recupera trechos delimitados e gera resposta. **Dificuldade:** Alta neste recorte.<br>**Vantagens:** Linguagem flexível e resposta fluida. **Limites:** Custo/recursos, falhas, avaliação e autoria mais difíceis de isolar.<br>**Dados:** Coleção curada, recuperação própria e avaliação. **Teste e defesa:** Mais difícil reproduzir e explicar integralmente.<br>**Adequação:** Permitida com recuperação/regras próprias; LLM isolado não cumpre R3.

Quantidades de exemplos são recomendações de partida, não mínimos oficiais nem garantia de desempenho. A nomenclatura de letras das opções varia entre os materiais; este plano identifica cada arquitetura pelo nome para evitar confusão.

## 9. Arquitetura recomendada e aprovada

**Decisão da equipe:** arquitetura híbrida com TF-IDF e similaridade para interpretação, regras para parâmetros/contexto/fallback, Open Library para metadados e templates para resposta. Não há LLM no fluxo do MVP.

**Autoria identificável:** construir corpus, normalizar, ajustar vocabulário/IDF no treino, comparar mensagens, agregar scores por intenção, definir política, extrair parâmetros, resolver diálogo e avaliar. Bibliotecas são meios permitidos; a equipe não precisa reimplementar a biblioteca, mas deve explicar seu uso e os trechos autorais.

### Pontuação e decisão

**Recomendação técnica:** usar a média das três maiores similaridades entre exemplos de cada intenção. Comparar melhor score s1 com segundo score s2. Avaliar essa agregação contra usar somente o vizinho mais próximo. Valores de limiar τ e margem δ serão escolhidos na validação e congelados antes do teste final.

| Condição | Ação |
| --- | --- |
| s1 abaixo de τ | Abster-se ou solicitar reformulação |
| s1 suficiente, diferença s1-s2 abaixo de δ | Esclarecer as duas hipóteses |
| s1 e margem suficientes | Aceitar intenção candidata |
| Intenção aceita, parâmetro ausente | Solicitar o dado necessário |
| Intenção e parâmetros conflitantes | Confirmar antes de consultar |

Score de similaridade não é probabilidade: 0,70 não significa 70% de chance de acerto. A rejeição por baixa similaridade também não detecta perfeitamente todos os pedidos fora do domínio; pedidos operacionais conhecidos podem exigir regras explícitas e testes negativos.

### Parâmetros e regras de diálogo

- Trechos entre aspas podem indicar título; padrões “livros de” e “livros sobre” ajudam autor/assunto.

- ISBN usa padrão numérico e validação; pode ficar no incremento P1.

- “O segundo” usa a lista atual; respostas curtas usam pergunta pendente apenas quando inequívocas.

- Cancelar e nova solicitação explícita substituem estado pendente.

- Conflito entre evidências causa esclarecimento, não consulta arbitrária.

**Precedência:** validar entrada/cancelamento → resolver seleção inequívoca ou parâmetro pendente → interpretar nova solicitação → verificar score/margem → extrair parâmetros → consultar → normalizar → responder. Não remover palavras como “quem”, “sobre” ou “de” sem medir o efeito.

### Contexto mínimo

Guardar por sessão: intenção pendente, parâmetro solicitado, última lista, obra selecionada e estado de esclarecimento. A equipe decidiu execução local; recomenda-se memória em processo, sem cadastro nem histórico permanente. Não é necessária memória longa.

## 10. Fluxo completo e componentes

| Componente | Responsabilidade |
| --- | --- |
| Interface | Enviar mensagens, mostrar resultados, seleção e carregamento |
| Validador/pré-processador | Verificar entrada; normalizar sem perder original e entidades |
| Interpretador | Propor intenção e expor scores/exemplos próximos |
| Extrator | Obter título, autor, assunto, ISBN ou referência contextual |
| Diálogo e política | Controlar pendências, conflito, contexto, aceitação e abstenção |
| Serviço externo | Traduzir consulta, limitar chamadas e tratar HTTP/JSON |
| Normalizador | Distinguir obra/edição e campos ausentes |
| Templates | Formular resposta apenas com dados disponíveis e fonte |
| Registro técnico | Evidências de execução sem segredos/dados pessoais |

| Situação | Comportamento esperado |
| --- | --- |
| Baixa similaridade | Pedir reformulação ou indicar busca por título, autor ou assunto |
| Ambiguidade | Perguntar qual ação o usuário deseja |
| Dado ausente | Perguntar pelo título/autor/assunto |
| API indisponível | Informar falha da fonte e permitir nova tentativa |
| Sem resultado | Dizer que não encontrou nesta fonte e solicitar refinamento |
| Múltiplos candidatos | Mostrar lista numerada; pedir seleção antes de detalhar |
| Fora do escopo | Explicar limite e orientar atendimento da biblioteca quando adequado |
| Campo/capa ausente | Informar ausência do campo; preservar demais resultados |
| Referência sem contexto | Perguntar de qual livro está falando |
| Nova demanda explícita | Atualizar estado e não reutilizar busca anterior |

**Recomendação técnica:** mostrar até cinco candidatos por vez e disponibilizar modo técnico com scores, parâmetros e motivo da decisão. A orientação a bibliotecário é informativa; não há envio de mensagens nem integração com atendimento humano.

## 11. Estratégia de dados

| Camada | Dados e finalidade |
| --- | --- |
| Base da equipe | Perguntas rotuladas, exemplos esperados, vocabulário curado e regras: interpretar/documentar domínio |
| Open Library | Títulos, autores, IDs, assuntos, datas e recursos disponíveis: conhecimento bibliográfico |
| Artefatos de PLN | Vocabulário, IDF, vetores de referência, rótulos e limiares: comparar mensagens |
| Sessão | Lista, obra selecionada e pendência: continuidade curta |
| Avaliação | Entradas independentes, parâmetros e respostas esperadas: verificar comportamento |

Estrutura mínima de CSV: **texto,intencao**. Estrutura recomendada para controle: **id,texto,intencao,grupo_variacao,origem,split**. Entidades esperadas podem ficar em arquivo separado associado pelo ID.

Exemplos: “quero livros sobre inteligência artificial”, buscar_por_assunto; “quem escreveu dom casmurro”, consultar_detalhes; “procure livros de george orwell”, buscar_obras_autor. Não gerar centenas de frases artificiais antes de fechar o guia.

### Construção e curadoria

- Escrever definições, exemplos negativos e regras de anotação.

- Coletar 30-40 exemplos diversos por intenção como ponto de partida, distribuindo entre integrantes.

- Variar estrutura, verbos, formalidade, comprimento, títulos/autores e informação incompleta.

- Revisar rótulos em dupla; agrupar duplicatas e paráfrases; registrar divergências.

- Manter entradas ambíguas e fora do escopo em avaliação específica; não forçar todo caso difícil a uma intenção.

- Guardar origem, permissões, limpeza, possíveis vieses e exemplos representativos.

### Separação e prevenção de vazamento

**Recomendação técnica:** 60% referência/treino, 20% validação, 20% teste, com equilíbrio por intenção e separação por grupos de formulação. Ajustar vocabulário/IDF somente no treino. Validação escolhe configuração, agregação e limiares. Teste final mede versão congelada.

- Não dividir paráfrases quase idênticas entre conjuntos apenas por sorteio.

- Não ajustar limiares pelo teste nem usar frases do teste para calcular IDF.

- Trocar apenas nomes em uma frase pode continuar sendo vazamento de estrutura.

- Após usar erros do teste para melhorar, avaliar em novo conjunto independente e identificar a versão.

- No motor por similaridade, corpus é coleção de referência rotulada; não alegar treino supervisionado de regressão logística inexistente.

Versionar CSV/JSON pequenos no Git, com guia de anotação, grupos, origem e manifesto do split. Artefatos devem registrar dataset, biblioteca e configuração. Recursos externos, especialmente capas/descrições, não são automaticamente livres para redistribuição. Guardar somente o que for autorizado ou orientar recriação.

## 12. Estratégia da API pública

| Aspecto | Google Books, alternativa | Open Library, escolhida |
| --- | --- | --- |
| Chave | Documentação orienta chave/token para identificação de dados públicos | Leituras públicas do recorte não requerem chave |
| Limites | Quota efetiva depende do projeto; verificar documentação/console | Diretriz consultada: 1 req/s sem identificação; 3 req/s identificado |
| Título/autor/assunto | intitle:, inauthor:, subject: | title, author e consulta por assunto |
| ISBN | isbn: | Busca de identificador/edição |
| Descrição/capa | Campos opcionais no volume | Descrição pode exigir detalhe; capa por API específica |
| Modelagem | Volumes | Obras e edições distintas |
| Integração | Muitos campos em um recurso; credenciais exigem planejamento | Busca + detalhe quando necessário; execução sem segredo |
| Qualidade | Cobertura no recorte precisa ser medida | Também exige sondagem em português |

**Decisão da equipe:** Open Library como única API do MVP. A escolha favorece reprodução sem credenciais privadas e descoberta educacional. O trade-off é lidar com campos incompletos, consultas complementares e cobertura em português não garantida. Uma segunda fonte amplia reconciliação e testes; não está no MVP.

### Sondagem e integração

- Executar 10-15 consultas de literatura brasileira, autores internacionais, gêneros, assuntos acadêmicos e edições. Registrar cobertura e campos.

- Documentar limitações encontradas e revisar o recorte com o professor se a fonte não o sustentar; não migrar de API silenciosamente.

- Usar requisições de leitura, parâmetros codificados, timeout configurável e seleção mínima de campos.

- Tratar 429, 5xx, rede, JSON inválido, vazio e campos ausentes.

- Aplicar limite compartilhado entre sessões; evitar que busca e detalhe excedam a política.

- Usar retentativas limitadas para falhas apropriadas e respeitar Retry-After quando informado.

- Identificar aplicação conforme diretrizes; usar contato autorizado da equipe. Não inventar endereço.

- Cachear consultas repetidas e não fazer coleta em massa por chamadas individuais.

**Pendente na implementação:** conferir limites vigentes, sintaxe de assunto/ISBN, esquema, idioma, condições de uso e política de capas. A API fornece informações; ela não é o mecanismo de IA. Busca/descrição/capa não garante disponibilidade no acervo local.

## 13. Estratégia de testes e métricas

**Exigência do professor:** 20+ perguntas, esperado/obtido/resultado, métricas adequadas e 3 falhas analisadas. **Recomendação técnica:** separar interpretação, diálogo e integração. Todos os casos a seguir estão planejados e não executados.

### Casos T01 a T12

| ID / entrada | Intenção esperada | Comportamento esperado |
| --- | --- | --- |
| T01<br>Procure Dom Casmurro | buscar_por_titulo | Consultar título e listar candidatos |
| T02<br>Você encontra o livro A Hora da Estrela? | buscar_por_titulo | Extrair título sem comando |
| T03<br>Estou atrás de um livro chamado 1984 | buscar_por_titulo | Reconhecer reformulação |
| T04<br>Procure Dom Casmuro | buscar_por_titulo | Buscar grafia ou confirmar; não inventar correspondência |
| T05<br>Quais livros Machado de Assis escreveu? | buscar_obras_autor | Consultar autor e listar obras |
| T06<br>Mostre obras de Clarice Lispector | buscar_obras_autor | Extrair nome completo |
| T07<br>Quero ler algo escrito por George Orwell | buscar_obras_autor | Reconhecer reformulação |
| T08<br>Quero livros sobre inteligência artificial | buscar_por_assunto | Consultar tema |
| T09<br>Me mostre ficção científica | buscar_por_assunto | Reconhecer gênero |
| T10<br>Alguma leitura a respeito de astronomia? | buscar_por_assunto | Reconhecer reformulação |
| T11<br>Quem escreveu Dom Casmurro? | consultar_detalhes | Resolver obra e informar autoria da fonte |
| T12<br>Quero saber mais sobre A Hora da Estrela | consultar_detalhes | Mostrar detalhes ou pedir seleção |

### Casos T13 a T24

| ID / entrada | Intenção esperada | Comportamento esperado |
| --- | --- | --- |
| T13<br>Livros de história | Assunto ou esclarecimento | Fixar política antes de executar; não alterar oráculo depois |
| T14<br>Machado | Esclarecimento | Pedir nome completo ou confirmar hipótese |
| T15<br>Busque um livro | buscar_por_titulo, incompleta | Perguntar título |
| T16<br>Mostre livros de um autor | buscar_obras_autor, incompleta | Perguntar autor |
| T17<br>Qual a previsão do tempo? | Fora do escopo | Abster-se e explicar domínio |
| T18<br>Renove meu empréstimo | Fora do escopo operacional | Explicar limite e orientar biblioteca |
| T19<br>Procure Zyx Livro 8472 | buscar_por_titulo | Com vazio controlado, informar ausência na fonte |
| T20<br>Obras de Zyx Autor 8472 | buscar_obras_autor | Com vazio controlado, pedir revisão do nome |
| T21<br>Procure 1984 | buscar_por_titulo | Com timeout simulado, informar indisponibilidade |
| T22<br>Procure Dom Casmurro | buscar_por_titulo | Com múltiplos resultados, listar e pedir seleção |
| T23<br>Busca → o segundo → quem escreveu? | Seleção + detalhes | Usar item selecionado na sessão |
| T24<br>Orwell → Agora quero livros sobre astronomia | buscar_por_assunto | Trocar demanda sem reutilizar autor |

Na tabela de execução, acrescentar colunas **Resultado obtido** e **Passou?**, atualmente “Não executado” e “-”. Registrar versão, estado inicial, parâmetros esperados e modo controlado/ao vivo. T13 deve ter política congelada antes da execução. Livro/autor inventado no teste não prova inexistência universal; o retorno vazio é controlado.

Nos testes automatizados, usar respostas externas controladas com IDs e dados definidos. Em integração ao vivo, verificar consultas e identificadores sem exigir ordem fixa de um catálogo mutável. Acrescentar 429, seleção inválida, campo ausente, ISBN e pergunta sem contexto quando esses comportamentos forem implementados.

| Métrica | Aplicação e cuidado |
| --- | --- |
| Taxa geral de sucesso | Casos com comportamento correto / casos executados; abstenção correta pode passar |
| Accuracy de intenção | Rótulos corretos / entradas independentes com rótulo único; não misturar ambiguidades |
| Precision e recall | Por intenção, para identificar previsões indevidas e classes não recuperadas |
| F1 e macro-F1 | Combinar precision/recall e dar peso semelhante às classes |
| Matriz de confusão | Observar confusão entre título, autor, assunto e detalhes; registrar rejeições |
| Taxa de fallback | Separar correto de desnecessário; baixa taxa não significa qualidade |
| Acerto de parâmetros | Verificar extração independentemente da intenção |
| Rejeição fora do escopo | Avaliar rejeições corretas e aceitações indevidas |
| Latência, opcional | Separar tempo local e externo; verificar usabilidade |

As métricas de classificação são aplicáveis ao motor de similaridade porque ele retorna rótulos. Similaridade média pode ser diagnóstico, mas não substitui correção. Mostrar contagens e denominadores, não só percentuais. Avaliar exemplos conhecidos não demonstra generalização.

### Análise de falhas e melhoria

Para cada uma das três falhas reais: entrada; esperado/obtido; scores/parâmetros/contexto; causa provável; impacto; correção proposta; resultado após correção, se executada. Se a suíte principal não revelar três erros, ampliar com casos difíceis e registrar honestamente os encontrados. Não fabricar resultados nem usar falhas simuladas da API como substituto automático de erros reais da avaliação.

## 14. Backlog completo

**Recomendação técnica:** IDs B01-B39 organizam o trabalho. Responsável de todas as tasks: **a definir**. Dificuldade B/M/A significa baixa/média/alta relativa à equipe. P0 obrigatório ao MVP/atividade; P1 importante; P2 melhoria; P3 diferencial. Cada task abaixo contém descrição/objetivo, aceite, dependências, prioridade, dificuldade, requisito e evidência.

| EPIC | Área | FEATUREs |
| --- | --- | --- |
| E1 | Problema e requisitos | F1.1 cenário; F1.2 escopo; F1.3 rastreabilidade |
| E2 | Dados | F2.1 corpus; F2.2 curadoria; F2.3 separação/versionamento |
| E3 | Arquitetura | F3.1 fluxo; F3.2 contratos; F3.3 decisões |
| E4 | IA/PLN e diálogo | F4.1 interpretação; F4.2 parâmetros; F4.3 contexto/fallback |
| E5 | Fonte externa | F5.1 pesquisa; F5.2 cliente; F5.3 normalização/robustez |
| E6 | Aplicação | F6.1 backend; F6.2 interface; F6.3 execução |
| E7 | Avaliação | F7.1 testes; F7.2 métricas; F7.3 falhas |
| E8 | Entrega e defesa | F8.1 relatório; F8.2 pacote; F8.3 apresentação/estudo |

### B01 • Definir cenário

**FEATURE:** F1.1 • **Prioridade:** P0 • **Dificuldade:** B • **Responsável:** a definir

**Descrição e objetivo:** Registrar público, necessidade e quatro problemas para delimitar a proposta.<br>**Aceite:** Nome, público, cenário, objetivo, limites e 10 perguntas presentes.<br>**Dependências:** -.<br>**Requisito:** C2 / Marco 1. **Evidência:** Ficha do problema.

### B02 • Fixar escopo e intenções

**FEATURE:** F1.2 • **Prioridade:** P0 • **Dificuldade:** M • **Responsável:** a definir

**Descrição e objetivo:** Formalizar as quatro ações e exclusões aprovadas.<br>**Aceite:** Definições com positivos, negativos e ambiguidades.<br>**Dependências:** B01.<br>**Requisito:** R2. **Evidência:** Catálogo de intenções.

### B03 • Mapear requisitos

**FEATURE:** F1.3 • **Prioridade:** P0 • **Dificuldade:** B • **Responsável:** a definir

**Descrição e objetivo:** Associar entregas e evidências à rubrica.<br>**Aceite:** Todo requisito possui ação e evidência planejadas.<br>**Dependências:** B01.<br>**Requisito:** R1-R7. **Evidência:** Matriz de rastreabilidade.

### B04 • Validar cobertura da API

**FEATURE:** F5.1 • **Prioridade:** P0 • **Dificuldade:** M • **Responsável:** a definir

**Descrição e objetivo:** Sondar Open Library com consultas do recorte.<br>**Aceite:** 10-15 consultas registradas, campos/limites documentados, limitações identificadas.<br>**Dependências:** B01.<br>**Requisito:** Marco 2 / API do projeto. **Evidência:** Registros de sondagem.

### B05 • Criar guia de anotação

**FEATURE:** F2.1 • **Prioridade:** P0 • **Dificuldade:** M • **Responsável:** a definir

**Descrição e objetivo:** Padronizar rótulos e reduzir divergência.<br>**Aceite:** Dois integrantes revisam amostra e resolvem divergências pelas regras.<br>**Dependências:** B02.<br>**Requisito:** R2 / Marco 2. **Evidência:** Guia versionado.

### B06 • Construir corpus

**FEATURE:** F2.1 • **Prioridade:** P0 • **Dificuldade:** M • **Responsável:** a definir

**Descrição e objetivo:** Coletar frases diversas para interpretação.<br>**Aceite:** Quatro intenções cobertas; origem registrada; volume inicial justificado.<br>**Dependências:** B05.<br>**Requisito:** R2-R3. **Evidência:** CSV e exemplos esperados.

### B07 • Curar dados

**FEATURE:** F2.2 • **Prioridade:** P0 • **Dificuldade:** M • **Responsável:** a definir

**Descrição e objetivo:** Revisar duplicatas, rótulos, grupos e permissões.<br>**Aceite:** Divergências resolvidas; grupos identificados; sem dados pessoais desnecessários.<br>**Dependências:** B06.<br>**Requisito:** Marco 2. **Evidência:** Histórico de limpeza.

### B08 • Separar conjuntos

**FEATURE:** F2.3 • **Prioridade:** P0 • **Dificuldade:** M • **Responsável:** a definir

**Descrição e objetivo:** Congelar referência, validação e teste sem vazamento.<br>**Aceite:** Grupos separados; equilíbrio documentado; versão registrada.<br>**Dependências:** B07.<br>**Requisito:** R5-R6. **Evidência:** Splits e manifesto.

### B09 • Desenhar arquitetura

**FEATURE:** F3.1 • **Prioridade:** P0 • **Dificuldade:** M • **Responsável:** a definir

**Descrição e objetivo:** Definir componentes, fluxo e comparação.<br>**Aceite:** Diagrama, alternativa, responsabilidade e fallback explicados.<br>**Dependências:** B02, B04.<br>**Requisito:** Marco 3. **Evidência:** Diagrama e decisão.

### B10 • Definir contratos

**FEATURE:** F3.2 • **Prioridade:** P0 • **Dificuldade:** M • **Responsável:** a definir

**Descrição e objetivo:** Especificar mensagem, interpretação, livro e sessão para integração.<br>**Aceite:** Campos obrigatórios/opcionais, erros e exemplos definidos.<br>**Dependências:** B09.<br>**Requisito:** R4. **Evidência:** Schemas e exemplos.

### B11 • Preparar projeto

**FEATURE:** F3.3 • **Prioridade:** P0 • **Dificuldade:** B • **Responsável:** a definir

**Descrição e objetivo:** Organizar ambiente, pastas e dependências.<br>**Aceite:** Instalação mínima reproduzida e estrutura registrada.<br>**Dependências:** B09.<br>**Requisito:** R7. **Evidência:** Configuração/README inicial.

### B12 • Criar fluxo vertical simulado

**FEATURE:** F6.1 • **Prioridade:** P0 • **Dificuldade:** M • **Responsável:** a definir

**Descrição e objetivo:** Conectar interface, backend, serviço e resposta cedo.<br>**Aceite:** Uma mensagem percorre todas as camadas com dados controlados.<br>**Dependências:** B10, B11.<br>**Requisito:** R1, R4. **Evidência:** Demo inicial sem alegar R3 completo.

### B13 • Pré-processar texto

**FEATURE:** F4.1 • **Prioridade:** P0 • **Dificuldade:** M • **Responsável:** a definir

**Descrição e objetivo:** Normalizar de modo consistente sem destruir entidades.<br>**Aceite:** Mesmo tratamento no ajuste e uso; original preservado.<br>**Dependências:** B08, B10.<br>**Requisito:** R3-R4. **Evidência:** Exemplos antes/depois.

### B14 • Implementar similaridade

**FEATURE:** F4.1 • **Prioridade:** P0 • **Dificuldade:** M • **Responsável:** a definir

**Descrição e objetivo:** Ajustar TF-IDF e gerar pontuações por intenção.<br>**Aceite:** Teste não participa do ajuste; decisão e vizinhos rastreáveis.<br>**Dependências:** B13.<br>**Requisito:** R3. **Evidência:** Código e execução técnica.

### B15 • Definir limiares

**FEATURE:** F4.3 • **Prioridade:** P0 • **Dificuldade:** M • **Responsável:** a definir

**Descrição e objetivo:** Selecionar política de aceitação, margem e abstenção.<br>**Aceite:** Configuração escolhida na validação e congelada.<br>**Dependências:** B14.<br>**Requisito:** R4, R6. **Evidência:** Comparação de configurações.

### B16 • Extrair parâmetros

**FEATURE:** F4.2 • **Prioridade:** P0 • **Dificuldade:** M • **Responsável:** a definir

**Descrição e objetivo:** Obter título, autor, assunto e referência contextual.<br>**Aceite:** Casos definidos corretos; falta ou conflito gera pergunta.<br>**Dependências:** B10, B13.<br>**Requisito:** R4. **Evidência:** Casos de extração.

### B17 • Gerenciar diálogo

**FEATURE:** F4.3 • **Prioridade:** P0 • **Dificuldade:** A • **Responsável:** a definir

**Descrição e objetivo:** Controlar perguntas pendentes e mudança de contexto.<br>**Aceite:** Seleção, cancelamento e nova busca sem estado indevido.<br>**Dependências:** B15, B16.<br>**Requisito:** R1, R4. **Evidência:** Diálogos completos.

### B18 • Implementar cliente externo

**FEATURE:** F5.2 • **Prioridade:** P0 • **Dificuldade:** M • **Responsável:** a definir

**Descrição e objetivo:** Traduzir consultas para a Open Library.<br>**Aceite:** Título/autor/assunto/detalhe funcionam; timeout e limite básico tratados.<br>**Dependências:** B04, B10, B11.<br>**Requisito:** R4 / API do projeto. **Evidência:** Consultas sem segredos.

### B19 • Normalizar livros

**FEATURE:** F5.3 • **Prioridade:** P0 • **Dificuldade:** M • **Responsável:** a definir

**Descrição e objetivo:** Converter campos externos para modelo consistente.<br>**Aceite:** Campos ausentes não quebram app; obra/edição e IDs preservados.<br>**Dependências:** B18.<br>**Requisito:** R4. **Evidência:** Exemplos normalizados.

### B20 • Tratar exceções

**FEATURE:** F5.3 • **Prioridade:** P0 • **Dificuldade:** M • **Responsável:** a definir

**Descrição e objetivo:** Lidar com vazio, múltiplos resultados e erro externo.<br>**Aceite:** Fluxo não inventa dados nem gera falha sem tratamento.<br>**Dependências:** B17, B19.<br>**Requisito:** R4 / protótipo. **Evidência:** Testes controlados.

### B21 • Integrar fluxo completo

**FEATURE:** F6.1 • **Prioridade:** P0 • **Dificuldade:** A • **Responsável:** a definir

**Descrição e objetivo:** Conectar PLN, diálogo, fonte e resposta.<br>**Aceite:** Quatro intenções funcionam ponta a ponta.<br>**Dependências:** B12, B17, B20.<br>**Requisito:** R1-R4. **Evidência:** Demo integrada.

### B22 • Finalizar interface

**FEATURE:** F6.2 • **Prioridade:** P0 • **Dificuldade:** M • **Responsável:** a definir

**Descrição e objetivo:** Tornar chat, lista, seleção e fonte utilizáveis.<br>**Aceite:** Usuário completa tarefas sem acesso ao código.<br>**Dependências:** B12, B10; finalizar após B21.<br>**Requisito:** R1. **Evidência:** Screenshots com contexto.

### B23 • Cache e retentativas

**FEATURE:** F5.3 • **Prioridade:** P1 • **Dificuldade:** M • **Responsável:** a definir

**Descrição e objetivo:** Reduzir chamadas e melhorar recuperação de falhas transitórias.<br>**Aceite:** Validade definida; retentativas limitadas respeitam fonte.<br>**Dependências:** B18, B20.<br>**Requisito:** Robustez recomendada. **Evidência:** Registros comparativos.

### B24 • Rastrear decisão

**FEATURE:** F4.1 • **Prioridade:** P1 • **Dificuldade:** B • **Responsável:** a definir

**Descrição e objetivo:** Expor scores, parâmetros e motivo para defesa.<br>**Aceite:** Modo técnico compreensível sem segredos.<br>**Dependências:** B21.<br>**Requisito:** R3 / defesa. **Evidência:** Capturas de execução.

### B25 • Busca por ISBN

**FEATURE:** F4.2 • **Prioridade:** P1 • **Dificuldade:** M • **Responsável:** a definir

**Descrição e objetivo:** Adicionar identificação de edição.<br>**Aceite:** ISBN inválido tratado e edição correta identificada.<br>**Dependências:** B16, B19.<br>**Requisito:** Melhoria. **Evidência:** Testes de identificador.

### B26 • Adicionar capas

**FEATURE:** F6.2 • **Prioridade:** P2 • **Dificuldade:** B • **Responsável:** a definir

**Descrição e objetivo:** Melhorar identificação visual quando autorizado.<br>**Aceite:** Falha da imagem não afeta busca; condições verificadas.<br>**Dependências:** B19, B22.<br>**Requisito:** Melhoria. **Evidência:** Exemplo visual.

### B27 • Preparar testes

**FEATURE:** F7.1 • **Prioridade:** P0 • **Dificuldade:** M • **Responsável:** a definir

**Descrição e objetivo:** Definir entradas, pré-condições e oráculos antecipadamente.<br>**Aceite:** 24 casos cobrem cenários oficiais; respostas controladas identificadas.<br>**Dependências:** B02, B10.<br>**Requisito:** R5. **Evidência:** Plano e fixtures.

### B28 • Executar avaliação

**FEATURE:** F7.1 • **Prioridade:** P0 • **Dificuldade:** M • **Responsável:** a definir

**Descrição e objetivo:** Avaliar interpretação, diálogo e integração.<br>**Aceite:** Resultados reais e falhas registrados com versão/modo.<br>**Dependências:** B08, B21, B22, B27.<br>**Requisito:** R5. **Evidência:** Tabela executada.

### B29 • Calcular métricas

**FEATURE:** F7.2 • **Prioridade:** P0 • **Dificuldade:** M • **Responsável:** a definir

**Descrição e objetivo:** Medir sucesso e confusões reproduzíveis.<br>**Aceite:** Contagens, denominadores e matriz corretos.<br>**Dependências:** B28.<br>**Requisito:** R6. **Evidência:** Métricas e matriz.

### B30 • Analisar três falhas

**FEATURE:** F7.3 • **Prioridade:** P0 • **Dificuldade:** M • **Responsável:** a definir

**Descrição e objetivo:** Localizar causas e propor melhorias fundamentadas.<br>**Aceite:** Três erros reais com entrada, causa, impacto e ação.<br>**Dependências:** B28, B29.<br>**Requisito:** Marco 5. **Evidência:** Fichas de erro.

### B31 • Corrigir prioridades

**FEATURE:** F7.3 • **Prioridade:** P1 • **Dificuldade:** M • **Responsável:** a definir

**Descrição e objetivo:** Melhorar falhas importantes sem contaminar avaliação.<br>**Aceite:** Correções verificadas; versões e nova avaliação identificadas.<br>**Dependências:** B30.<br>**Requisito:** Qualidade. **Evidência:** Comparação entre versões.

### B32 • Validar instalação limpa

**FEATURE:** F6.3 • **Prioridade:** P0 • **Dificuldade:** M • **Responsável:** a definir

**Descrição e objetivo:** Comprovar reprodução pelo professor.<br>**Aceite:** Outro integrante executa README sem ajuda nem segredo privado.<br>**Dependências:** B21, B28.<br>**Requisito:** R7. **Evidência:** Registro de reprodução.

### B33 • Redigir relatório

**FEATURE:** F8.1 • **Prioridade:** P0 • **Dificuldade:** A • **Responsável:** a definir

**Descrição e objetivo:** Consolidar análise e evidências oficiais.<br>**Aceite:** 6+ páginas efetivas; identificação, fontes, IA generativa e contribuições.<br>**Dependências:** B03; conclusão após B29, B30, B32.<br>**Requisito:** C7 / relatório. **Evidência:** PDF ou DOCX final.

### B34 • Preparar pacote

**FEATURE:** F8.2 • **Prioridade:** P0 • **Dificuldade:** B • **Responsável:** a definir

**Descrição e objetivo:** Revisar acesso, dados, código e versão final.<br>**Aceite:** Repositório/ZIP sem chaves e com dados ou recriação.<br>**Dependências:** B32, B33.<br>**Requisito:** C8 / entrega. **Evidência:** Pacote revisado.

### B35 • Slides e demonstração

**FEATURE:** F8.3 • **Prioridade:** P0 • **Dificuldade:** M • **Responsável:** a definir

**Descrição e objetivo:** Explicar problema, IA, decisões, resultados e limites.<br>**Aceite:** Roteiro cobre elementos oficiais e mostra erro analisado.<br>**Dependências:** B21, B29, B30.<br>**Requisito:** C9 / defesa. **Evidência:** Slides e roteiro.

### B36 • Ensaiar defesa

**FEATURE:** F8.3 • **Prioridade:** P0 • **Dificuldade:** M • **Responsável:** a definir

**Descrição e objetivo:** Preparar todos para pergunta inédita e autoria.<br>**Aceite:** Todos explicam contribuição e fluxo; ensaio cronometrado.<br>**Dependências:** B35.<br>**Requisito:** C1, C9. **Evidência:** Registro do ensaio.

### B37 • Preparar contingência

**FEATURE:** F8.3 • **Prioridade:** P1 • **Dificuldade:** B • **Responsável:** a definir

**Descrição e objetivo:** Manter demonstração técnica se internet falhar.<br>**Aceite:** Modo controlado identificado; não apresentado como consulta ao vivo.<br>**Dependências:** B20, B35.<br>**Requisito:** Robustez da defesa. **Evidência:** Plano alternativo.

### B38 • Comparar classificador

**FEATURE:** F4.1 • **Prioridade:** P2 • **Dificuldade:** A • **Responsável:** a definir

**Descrição e objetivo:** Experimentar alternativa se confusões justificarem.<br>**Aceite:** Validação independente sustenta adoção ou descarte.<br>**Dependências:** B29, B30.<br>**Requisito:** Melhoria experimental. **Evidência:** Comparativo.

### B39 • Recomendação por conteúdo

**FEATURE:** F4.1 • **Prioridade:** P3 • **Dificuldade:** A • **Responsável:** a definir

**Descrição e objetivo:** Criar ranking explicável somente após MVP.<br>**Aceite:** Dados, critério próprio e avaliação adicional definidos.<br>**Dependências:** MVP e entregas obrigatórias concluídos.<br>**Requisito:** Diferencial fora do MVP. **Evidência:** Ranking e testes.

### SUBTASKs de referência

| Task | Passos menores |
| --- | --- |
| B06 | B06.1 distribuir coleta; B06.2 revisar rótulos; B06.3 agrupar paráfrases; B06.4 registrar origem/versão |
| B14 | B14.1 ajustar TF-IDF no treino; B14.2 transformar mensagens; B14.3 cosseno; B14.4 agregar classes; B14.5 rastrear vizinhos |
| B18 | B18.1 título; B18.2 autor; B18.3 assunto; B18.4 detalhe por ID; B18.5 timeout/limite |
| B28 | B28.1 interpretação independente; B28.2 diálogos controlados; B28.3 consultas reais; B28.4 revisão por outro integrante |
| B33 | B33.1 problema/requisitos; B33.2 dados/IA; B33.3 implementação; B33.4 resultados/falhas; B33.5 conclusão/fontes/autoria; B33.6 verificar conteúdo efetivo |

## 15. Roadmap, desenvolvimento e tecnologias

| Fase | Área | Tasks | Saída |
| --- | --- | --- | --- |
| 1 | Definição do problema | B01-B03 | Marco 1 |
| 2 | Pesquisa e dados | B04-B08 | Marco 2; corpus versionado |
| 3 | Arquitetura | B09-B11 | Marco 3; contratos |
| 4 | IA/PLN | B13-B17 | Interpretador e diálogo |
| 5 | Integração com API | B18-B20; B23 | Cliente e normalização |
| 6 | Backend | B12, B21 | Fluxo executável |
| 7 | Interface | B22; B26 | Chat utilizável |
| 8 | Testes | B27, B28, B32 | Casos executados e reprodução |
| 9 | Avaliação | B29-B31 | Marco 5; métricas e falhas |
| 10 | Relatório | B33, B34 | Relatório e pacote |
| 11 | Apresentação e defesa | B35-B37 | Marco 6; demo e desafio |

**Dependências:** problema → dados e arquitetura em paralelo; contratos → protótipo simulado, IA, cliente e interface; integração completa → avaliação; resultados → relatório final e defesa. Não há datas porque o calendário dos marcos ainda não foi informado.

**Ordem recomendada:** fluxo vertical com dados simulados → PLN real → API real → quatro intenções integradas → contexto/robustez → avaliação → consolidação documental → ensaio. O protótipo simulado é provisório e ainda não atende sozinho ao mecanismo de IA. Testes, referências e documentação começam cedo.

| Frente de trabalho | Tasks paralelas e condição |
| --- | --- |
| Dados e PLN | B05-B08, B13-B15; requer intenções e guia |
| API | B04, B18-B20; requer modelo de livro |
| Backend e diálogo | B10-B12, B16-B17, B21; requer contratos |
| Interface, avaliação e documentação | B22, B27 e registro de evidências; requer contrato de mensagens |

Com duas pessoas, combinar frentes; com quatro, atribuir uma frente principal por pessoa. Revisão cruzada continua necessária. Cargo não comprova autoria: guardar implementações, testes, revisões e contribuições.

### Escolha de linguagem e ferramentas

| Opção | Adequação a este projeto |
| --- | --- |
| Python, escolhido | Integra PLN, experimentos e métricas com scikit-learn; facilita pipeline local |
| Java, alternativa | Viável com Spring Boot, cliente HTTP e biblioteca/estruturas de PLN; favorece equipe já experiente, mas pode exigir mais montagem experimental |

| Ferramenta | Necessidade concreta / estado |
| --- | --- |
| Python | Linguagem aprovada |
| scikit-learn | TF-IDF, cosseno e métricas; recomendado |
| FastAPI | Contrato e validação do backend; recomendado, Flask é alternativa |
| httpx | HTTP com timeout e tratamento de erro; recomendado |
| HTML/CSS/JavaScript | Chat simples; aprovado como interface, sem framework obrigatório |
| CSV/JSON e Git | Dados pequenos, regras e versões; recomendado |
| pytest | Testes com entradas e respostas controladas; recomendado |
| pandas, opcional | Tabulação experimental se necessário |
| Banco de dados/LLM | Não necessários no MVP |

### Estrutura de pastas proposta

biblioteca-capitu/<br> README.md \| pyproject.toml \| .env.example<br> app/<br> main.py \| schemas.py<br> nlp/ preprocessing.py \| intent_similarity.py \| entity_extraction.py<br> dialogue/ manager.py \| context.py \| policy.py<br> services/ open_library.py \| normalization.py \| cache.py<br> responses/ templates.py<br> static/ index.html \| styles.css \| chat.js<br> data/ README.md \| annotation_guide.md \| intents.csv \| subjects.json<br> splits/<br> artifacts/ README.md<br> evaluation/ test_cases.csv \| results/ \| error_analysis.md<br> tests/ fixtures/ \| test_intents.py \| test_dialogue.py \| test_api_service.py<br> scripts/ build_index.py \| evaluate.py<br> docs/ requirements.md \| architecture.md \| decisions/ \| evidence/<br> report/ \| presentation/

Estrutura planejada, não criada como implementação. Versões exatas de linguagem/bibliotecas serão registradas na preparação do ambiente. FastAPI e httpx são recomendações ainda não confirmadas nominalmente pela equipe.

## 16. Riscos

| Risco | Probabilidade | Impacto | Mitigação |
| --- | --- | --- | --- |
| API fora do ar | Média | Alto | Timeout, fallback e contingência controlada |
| Limite da API | Média | Médio/alto | Limitador compartilhado, cache e poucas chamadas |
| Cobertura em português | Média | Alto | Sondagem antecipada; registrar limites do recorte |
| Intenção incorreta | Alta no início | Alto | Diversidade, matriz de confusão e abstenção |
| Dataset pequeno | Média | Alto | Ampliar variedade a partir de falhas |
| Overfitting de formulações | Média | Alto | Grupos separados e perguntas inéditas |
| Data leakage | Média | Alto | Ajuste só no treino; congelar conjuntos |
| Ambiguidade | Alta | Médio | Esclarecimento e catálogo de rótulos |
| Entidade incorreta | Média | Alto | Extração delimitada e confirmação |
| Campo/resultado vazio | Alta | Médio | Normalização opcional e mensagens específicas |
| Obra versus edição | Média | Alto | Preservar IDs e rotular datas/ISBN |
| Contexto indevido | Média | Médio/alto | Estado explícito e testes de troca |
| Excesso de IA generativa | Baixa no desenho | Alto | MVP sem LLM; declarar apoio efetivo |
| Complexidade excessiva | Média | Alto | Congelar MVP e adiar diferenciais |
| Defesa sem compreensão | Média | Alto | Rastreamento, revisão e ensaio |
| Execução em outro ambiente | Média | Alto | Instalação limpa pelo README |
| Autoria não comprovada | Média | Alto | Tasks, commits e contribuições |
| Métricas pouco representativas | Média | Alto | Separar avaliações e apresentar amostra |
| Esquema externo muda | Baixa/média | Médio | Adaptador isolado e validação |
| Prazo insuficiente | A estimar | Alto | Confirmar calendário e cortar P2/P3 |

Probabilidades/impactos são estimativas de planejamento, não resultados de análise quantitativa. Revisar no Marco 5.

## 17. Evidências, relatório e preparação da defesa

| Seção obrigatória do relatório | Evidências a guardar |
| --- | --- |
| 1. Introdução e problema | Cenário, público, quatro problemas, perguntas, objetivo e limites |
| 2. Requisitos e casos de uso | Matriz R1-R7, intenções, negativos, diálogos e critérios de aceite |
| 3. Dados e conhecimento | Corpus, origem/permissão, limpeza, guia, grupos, split, versão e vieses |
| 4. Arquitetura e técnica de IA | Diagrama, algoritmo, alternativa, decisão, scores e limiares |
| 5. Implementação | Ambiente, versões, componentes, trechos autorais curtos e execução |
| 6. Experimentos e avaliação | 20+ testes, esperado/obtido, métricas, matriz e três falhas reais |
| 7. Discussão e conclusão | Valor observado, limites, riscos, orientação humana e evolução |
| Referências e contribuições | Documentos, API, bibliotecas, uso de IA generativa e autoria verificável |

- Registrar decisão e alternativa considerada, associando à task e ao commit.

- Guardar dataset/configuração/versão de cada execução.

- Salvar exemplos corretos e incorretos com scores, parâmetros e contexto.

- Registrar chamadas externas sem tokens, segredos ou dados pessoais.

- Identificar explicitamente demonstração controlada versus consulta ao vivo.

- Guardar screenshots explicados; não usá-los para substituir análise textual.

- Registrar contribuição individual, revisão e limitações.

- Atualizar README e preservar resultados de versões anteriores.

**Declaração de apoio nesta etapa:** este planejamento foi elaborado com auxílio de IA generativa na conversa, a partir dos documentos fornecidos e escolhas da equipe. Não houve implementação ou experimento. A declaração do relatório final deverá registrar os usos efetivamente realizados durante todo o desenvolvimento; a equipe responde por compreender, revisar e testar o material.

### Backlog de estudo para a defesa

| Tema | Perguntas para estudar |
| --- | --- |
| Arquitetura | Por que separar interpretação, diálogo e API? Quem decide a consulta? Como resolver conflito? |
| IA/similaridade | Onde está o mecanismo próprio? O que TF-IDF mede? Como funciona cosseno? Por que score não é probabilidade? Por que agregar três vizinhos? |
| Dados/ajuste | Quem criou e revisou? Como variar frases? Como evitar leakage? O que é aprendido no IDF? Como tratar nomes inéditos? |
| Classificação | Como a similaridade produz um rótulo? O que mudaria com regressão logística? Como avaliar rejeição? |
| API | Por que Open Library? O que falta no catálogo? Como tratar limites? Obra e edição são iguais? |
| Testes/métricas | O que significa passar? Accuracy e sucesso diferem? O que revelou a matriz? Como escolheram limiar? |
| Erros/fallback | Qual erro mais importante? Quando esclarecer? Fallback alto é ruim? Como agir sem internet? |
| Limites/autoria | Conhece acervo local? Como adicionar intenção? Que apoio de IA houve? O que cada integrante fez? Todos explicam o fluxo? |

**Recomendação técnica:** ensaiar pergunta inédita por integrante e mudança curta, como busca por ISBN. Apresentação sugerida no enunciado: cinco minutos de explicação/demo e três de perguntas, a confirmar com professor. Mostrar pelo menos uma falha analisada e a localização do mecanismo no código.

## 18. Decisões confirmadas e pendências

| Confirmado pela equipe | Escolha |
| --- | --- |
| Nome | CAPITU |
| Cenário | Biblioteca universitária simulada |
| Público/escopo | Descoberta bibliográfica; quatro intenções |
| Limites | Sem operação do acervo e sem personalização |
| Linguagem | Python |
| Arquitetura | Híbrida: TF-IDF + similaridade + regras |
| Fonte | Open Library |
| Interface/execução | Chat web simples e local |

| Momento | Questão, opções e recomendação |
| --- | --- |
| Agora | Integrantes (2-4), turma/curso/instituição e responsáveis: preencher antes de formalizar entregas |
| Agora | Calendário: obter prazos oficiais dos seis marcos; não inventar datas |
| Antes de integrar | FastAPI ou Flask; httpx ou requests: recomenda-se FastAPI/httpx por contrato e timeout |
| Antes de preparar dados | Regras de anotação e coleta autoral/colegas: recomenda-se revisão em dupla e origem registrada |
| Antes de validar | Agregação, limiares e margem: comparar candidatos na validação, sem usar teste |
| Depois | N-gramas de caracteres: adicionar se erros de grafia justificarem |
| Depois | Cache e validade: definir após observar chamadas e limites |
| Depois | ISBN, capas e filtros: incrementos P1/P2; não bloqueiam quatro intenções |
| Depois | Classificador alternativo: somente se ganho experimental justificar |
| Depois | Hospedagem e recomendação: fora do MVP; exigem nova decisão e avaliação |

**Validação solicitada ao professor:** adequação do recorte, das quatro intenções, do corpus próprio com fonte externa e do mecanismo de PLN; compatibilidade das evidências com A3; confirmação de prazos e eventuais ajustes. Aprovação da proposta não substitui avaliação da entrega final.

## 19. Próximos cinco passos

**1.** Enviar a proposta breve ao professor e registrar ajustes solicitados.

**2.** Confirmar integrantes, dados de identificação e calendário; atribuir tasks.

**3.** Concluir ficha do Marco 1 e sondar Open Library com consultas representativas.

**4.** Criar guia de anotação, corpus inicial e avaliação independente.

**5.** Fechar contratos e iniciar fluxo vertical simulado, seguido de PLN e API reais.

## Referências e documentos de apoio

**Documento oficial A3**<br>A3_Projeto_Chatbots_IA_40_pontos_20260923193204(2).docx. Documento fornecido pela estudante. Seções 1 a 11.

**Material complementar**<br>Marcelo da Silva. A3 Projeto Integrador de Inteligência Artificial: tecnologias possíveis e conceitos essenciais. PDF fornecido pela estudante, 23 páginas, 07/10/2026.

**Open Library: APIs e diretrizes**<br>[https://openlibrary.org/developers/api](https://openlibrary.org/developers/api)

**Open Library: Search API**<br>[https://openlibrary.org/dev/docs/api/search](https://openlibrary.org/dev/docs/api/search)

**Open Library: Books API**<br>[https://openlibrary.org/dev/docs/api/books](https://openlibrary.org/dev/docs/api/books)

**Open Library: Covers API**<br>[https://openlibrary.org/dev/docs/api/covers](https://openlibrary.org/dev/docs/api/covers)

**Open Library: licenciamento**<br>[https://openlibrary.org/developers/licensing](https://openlibrary.org/developers/licensing)

**Google Books: comparação de alternativa**<br>[https://developers.google.com/books/docs/v1/using](https://developers.google.com/books/docs/v1/using)

**scikit-learn: extração textual**<br>[https://scikit-learn.org/stable/modules/feature_extraction.html#text-feature-extraction](https://scikit-learn.org/stable/modules/feature_extraction.html#text-feature-extraction)

**scikit-learn: avaliação**<br>[https://scikit-learn.org/stable/modules/model_evaluation.html#classification-metrics](https://scikit-learn.org/stable/modules/model_evaluation.html#classification-metrics)

Os dois documentos do professor foram lidos integralmente. A documentação externa foi consultada durante o planejamento inicial; limites, esquema e condições de uso devem ser reconferidos na integração. Pesquisa documental não comprova disponibilidade ao vivo nem cobertura do catálogo.
