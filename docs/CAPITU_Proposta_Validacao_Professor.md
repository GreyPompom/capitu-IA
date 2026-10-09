# Proposta de implementação da CAPITU para validação do professor

> **Sincronização obrigatória: qualquer alteração neste documento deve ser reproduzida no PDF e no Markdown do mesmo nome-base antes do commit.**
> **PDF correspondente:** `CAPITU_Proposta_Validacao_Professor.pdf`

## Proposta para validação do professor

Chatbot inteligente de descoberta bibliográfica • Inteligência Artificial • Avaliação A3 de 40 pontos

**Destinatário:** Professor Marcelo da Silva<br>**Professor:** Marcelo da Silva<br>**Instituição, curso, turma e integrantes:** a definir<br>**Data:** 7 de outubro de 2026 • **Versão:** 1.0

**Estado do projeto:** planejamento anterior à implementação. As escolhas de cenário, escopo, limites, Python, arquitetura híbrida com TF-IDF, Open Library e chat web local foram confirmadas pela equipe nesta conversa. Protótipo, dataset, consultas experimentais e testes ainda serão desenvolvidos; não há resultados obtidos nesta versão.

**Solicitação:** validar o recorte, os objetivos e a solução técnica antes da implementação. A síntese abaixo também cobre a atividade de uma folha da página 22 da aula complementar: problema, intenções, arquitetura, justificativa e fallback.

### Problema e objetivo

Em uma biblioteca universitária simulada, estudantes precisam localizar obras a partir de títulos, autores ou assuntos, mas podem não saber formular buscas bibliográficas. A CAPITU será um assistente em português para interpretar esses pedidos, consultar a Open Library e apresentar resultados identificáveis, esclarecendo dúvidas quando necessário.

| Intenção | Dois exemplos de entrada |
| --- | --- |
| buscar_por_titulo | “Procure Dom Casmurro”; “Você encontra A Hora da Estrela?” |
| buscar_obras_autor | “Quais livros Machado de Assis escreveu?”; “Mostre obras de Clarice Lispector” |
| buscar_por_assunto | “Quero livros sobre IA”; “Mostre ficção científica” |
| consultar_detalhes | “Quem escreveu Dom Casmurro?”; “Qual o ISBN do segundo?” |

### Solução técnica escolhida

**Python + TF-IDF + similaridade cosseno + regras de diálogo + Open Library.** Chat web simples, executado localmente. FastAPI, scikit-learn, httpx e HTML/CSS/JavaScript são as ferramentas recomendadas para implementar as camadas.

**Fluxo:** mensagem → normalização → contexto/interpretação → limiar e extração de parâmetros → decisão → API de livros → normalização dos resultados → resposta com fonte.

**Justificativa:** permite implementar PLN próprio, inspecionar decisões, testar generalização e explicar o algoritmo sem custos de LLM ou complexidade desnecessária. A API fornece metadados; não será apresentada como mecanismo de IA.

**Fallback:** se a similaridade for baixa ou houver ambiguidade, pedir reformulação ou esclarecer título/autor/assunto. Se faltar dado, perguntar pelo parâmetro; se a fonte falhar, informar indisponibilidade.

**Limites:** não realizará empréstimos, reservas, consultas ao acervo institucional, compras ou recomendação personalizada. Não haverá LLM no MVP. A proposta está alinhada aos materiais; sua conformidade final dependerá da implementação e avaliação.

## Objetivos e escopo de desenvolvimento

**Objetivo geral:** desenvolver e avaliar um chatbot bibliográfico local, em português, com interpretação própria de solicitações, consulta à Open Library e tratamento explícito de incerteza.

- Implementar quatro intenções bibliográficas e ao menos um diálogo completo por intenção.

- Construir e versionar corpus próprio de perguntas; 30-40 exemplos por intenção são recomendação inicial.

- Executar ao menos 24 casos documentados, atendendo ao mínimo oficial de 20.

- Buscar 85% de sucesso funcional como meta interna, sem antecipar resultado.

- Demonstrar ambiguidade, ausência de resultados e falha externa sem inventar dados.

### Funcionamento da IA e contexto

O TF-IDF será ajustado sobre o corpus de referência/treino da equipe. Cada nova mensagem será comparada aos exemplos por similaridade cosseno; uma política aceitará a intenção, pedirá esclarecimento ou se absterá. Regras extrairão parâmetros e manterão a lista de resultados, obra selecionada e informação pendente na sessão.

**Precisão técnica:** trata-se de similaridade lexical, não compreensão semântica geral. Scores não são probabilidades. A média dos três exemplos mais próximos por intenção é uma hipótese inicial a validar; limiar e margem serão definidos em validação separada. Não haverá treino de classificador supervisionado no MVP.

### Dados e fonte externa

**Dados próprios:** perguntas rotuladas, exemplos esperados, vocabulário de assuntos e regras, com origem, limpeza e versões documentadas. **Dados externos:** metadados bibliográficos da Open Library, sujeitos a cobertura e campos ausentes. Descrições e capas só serão usadas quando disponíveis e conforme condições de uso.

A fonte foi escolhida por permitir consultas públicas sem chave privada e favorecer reprodução acadêmica. Antes da integração será feita sondagem com consultas em português. O cliente deverá respeitar limites, usar timeout e tratar erros. A fonte não representa o acervo da universidade.

### Alternativas e escolha

Regras isoladas seriam transparentes, mas frágeis a reformulações. Um classificador TF-IDF + regressão logística é alternativa futura caso os experimentos justifiquem. LLM + recuperação ampliaria custo e avaliação sem necessidade no recorte. A combinação escolhida prioriza simplicidade, autoria demonstrável e teste.

## Planejamento, avaliação e entregas

| Etapa | Entrega verificável |
| --- | --- |
| 1. Definição | Nome, público, cenário, quatro problemas, limites e 10 perguntas |
| 2. Dados | Corpus versionado, origem, preparação e avaliação independente |
| 3. Arquitetura | Fluxo, justificativa, alternativa e política de fallback |
| 4. Protótipo | Chat local, PLN próprio, API e instruções de execução |
| 5. Avaliação | 24 testes, métricas, 3 falhas reais e melhorias |
| 6. Defesa | Relatório, repositório/ZIP, apresentação e pergunta inédita |

A implementação seguirá: protótipo com dados simulados → PLN → API → robustez → avaliação → consolidação documental → defesa. Dados/PLN, serviço externo e interface podem ser desenvolvidos em paralelo após definir contratos. Os prazos dependem do calendário do professor.

### Método de validação

Separar corpus de referência/treino, validação e teste por grupos de formulação, evitando paráfrases quase idênticas em conjuntos diferentes. Ajustar TF-IDF e limiares sem usar o teste final. Cobrir perguntas diretas, reformulações, sinônimos, erros de grafia, ambiguidades, ausência de parâmetros, fora do escopo, retorno vazio, API indisponível, múltiplos resultados e mudança de contexto.

Registrar entrada, intenção esperada, comportamento esperado, resultado obtido e aprovação. Medir sucesso funcional, accuracy/precision/recall/F1 por intenção, matriz de confusão e taxa de fallback, com contagens e denominadores. Avaliação de classificação e avaliação de diálogo terão critérios separados. Não há testes executados nesta proposta.

### Entregas e autoria

Relatório final em PDF/DOCX com pelo menos seis páginas de conteúdo efetivo nas seções oficiais; código executável em repositório/ZIP sem segredos; README; corpus ou recriação autorizada; tabela de 20+ testes e métricas; apresentação com demonstração ao vivo. Todos os integrantes deverão explicar contribuição verificável e responder ao desafio reformulado.

**Riscos principais:** API indisponível/cobertura limitada; confusão de intenção; corpus pouco diverso; contexto incorreto; dificuldade de reprodução. Mitigações: sondagem, abstenção, revisão de dados, testes independentes e execução limpa.

### Pontos para validação do professor

- O cenário simulado e o recorte de descoberta bibliográfica são adequados à A3?

- As quatro intenções e os limites estão suficientemente delimitados?

- O corpus próprio e TF-IDF com política de decisão atendem ao mecanismo de PLN esperado?

- O plano de testes, métricas, três falhas e evidências é suficiente?

- Quais são os prazos dos marcos e eventuais ajustes exigidos?

**Pendências administrativas:** instituição, curso, turma, integrantes (2-4), responsáveis e calendário. **Apoio declarado:** proposta elaborada com auxílio de IA generativa; equipe responsável por revisar, compreender, implementar e testar.

## Fontes e verificação de alinhamento

A proposta foi confrontada com o enunciado oficial de 40 pontos e com as 23 páginas da aula do Professor Marcelo da Silva. A aula confirma intenções, entidades/contexto, base/dataset, TF-IDF, arquitetura híbrida, fallback, avaliação e defesa. Não acrescenta obrigação de LLM nem determina o limiar exemplificado de 0,70.

| Orientação | Tratamento na CAPITU |
| --- | --- |
| IA própria, além de serviço pronto | Pipeline autoral de interpretação e decisão, separado da API |
| 3+ intenções e contexto mínimo | Quatro intenções; seleção e esclarecimento na sessão |
| Dados e teste independente | Corpus rotulado e separação por grupos |
| 20+ testes e 3 falhas | 24 casos planejados e análise de erros reais |
| Explicação e pergunta inédita | Diagrama, rastreamento e ensaio de toda a equipe |
| Uma folha/slide na atividade rápida | Síntese apresentada na primeira página deste documento |

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

Esta versão breve serve para validação prévia. O planejamento detalhado da equipe contém backlog B01-B39, estratégia de dados, 24 casos de teste, riscos, evidências e roteiro de defesa. Nenhum dos dois documentos é o relatório final de resultados.
