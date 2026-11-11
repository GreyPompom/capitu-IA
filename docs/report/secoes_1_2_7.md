# Relatório Técnico CAPITU — Seções 1, 2 e Rascunho da 7

## 1. Problema, Público-Alvo e Objetivos

### 1.1 Definição do Problema

Em um cenário simulado de biblioteca universitária, estudantes e pesquisadores podem iniciar a descoberta bibliográfica com dados parciais ou descrições em linguagem natural, como "livro sobre inteligência artificial" ou "obras de Machado de Assis". A busca inicial pode se tornar difícil quando a pessoa não conhece o título completo, o nome preciso da autoria ou a terminologia de assunto usada pela fonte. A CAPITU intermedeia essa consulta bibliográfica em português, interpretando a intenção da pergunta antes de buscar metadados na fonte pública Open Library.

As demandas de atendimento delimitadas para o projeto são: localizar uma obra pelo título; listar obras associadas a um autor; descobrir obras por assunto ou gênero; e consultar detalhes disponíveis de uma obra identificada. O cenário é simulado e não representa nem confirma o acervo físico de uma instituição.

### 1.2 Público-Alvo

* **Usuários primários:** estudantes de graduação, pós-graduação e pesquisadores acadêmicos.
* **Necessidades:** descoberta de obras por tema, identificação de bibliografia associada a um autor e consulta a detalhes de livros por perguntas informais em português.

### 1.3 Objetivos do Sistema

* **Objetivo geral:** desenvolver e avaliar um chatbot bibliográfico em português, executado localmente, que interprete solicitações de busca e consulta de obras com PLN próprio, use a Open Library como fonte externa de metadados e trate incertezas de forma explícita.
* **Objetivos específicos:**
  1. Implementar quatro intenções operacionais e demonstrar ao menos um diálogo completo para cada uma.
  2. Extrair os parâmetros título, autor ou assunto quando necessários à consulta.
  3. Solicitar esclarecimento diante de ambiguidade ou parâmetro ausente, sem consultar a fonte prematuramente.
  4. Avaliar o protótipo com pelo menos 20 perguntas documentadas, incluindo reformulações, ambiguidades e itens fora do escopo.
  5. Garantir que a resposta não alegue acervo físico ou dados bibliográficos não fornecidos pela fonte externa.

## 2. Escopo, Intenções e Limitações do Domínio

### 2.1 Requisitos e Casos de Uso do MVP

| Caso de uso | Demanda atendida | Comportamento esperado | Limite ou encaminhamento |
| :--- | :--- | :--- | :--- |
| Buscar por título | Localizar uma obra por título completo ou parcial. | A CAPITU interpreta o pedido, extrai o título e apresenta candidatos retornados pela fonte. | Se não houver correspondência, informa somente que a fonte não retornou resultados e pede refinamento. |
| Buscar obras por autor | Consultar obras associadas a uma autoria. | A CAPITU extrai o nome do autor e apresenta resultados disponíveis. | Se o nome estiver ausente ou ambíguo, pede esclarecimento antes da consulta. |
| Buscar por assunto | Descobrir obras relacionadas a tema, assunto ou gênero. | A CAPITU extrai o assunto e apresenta resultados disponíveis. | Não produz recomendação personalizada nem afirma adequação pedagógica da obra. |
| Consultar detalhes | Obter metadados de uma obra identificada. | A CAPITU consulta detalhes disponíveis, como autoria, ano, descrição, editora ou ISBN quando a fonte os fornecer. | Havendo vários candidatos, solicita a seleção; campos ausentes permanecem como não informados. |

O sistema cobre exclusivamente descoberta de obras e consulta de metadados bibliográficos em fontes públicas abertas. A interface é um chat web executado localmente; o backend recebe cada turno em `POST /api/chat`.

### 2.2 As Quatro Intenções Consistentes

| Intenção | Descrição | Exemplo de requisição |
| :--- | :--- | :--- |
| `buscar_por_titulo` | Busca de obras pelo título parcial ou completo. | "Procure o livro Dom Casmurro" |
| `buscar_obras_autor` | Busca de obras associadas a um autor. | "Quais livros Machado de Assis escreveu?" |
| `buscar_por_assunto` | Localização de livros por tema, assunto ou gênero. | "Quero livros sobre inteligência artificial" |
| `consultar_detalhes` | Obtenção de metadados de uma obra identificada. | "Quem escreveu o livro O Alienista?" |

### 2.3 Limitações Explícitas do Domínio

* **Gestão física ausente:** o sistema não informa disponibilidade em estante, localização física, empréstimos, renovações ou multas.
* **Evidência obrigatória:** o sistema limita-se aos dados retornados pela Open Library. Nenhum resultado ou catálogo é inventado.
* **Sem personalização ou memória permanente:** o sistema não cria perfil, histórico permanente, recomendação personalizada ou decisão sobre o usuário.
* **Abstenção por baixa confiança:** requisições fora do escopo ou com evidência insuficiente na interpretação híbrida disparam mensagens de abstenção ou esclarecimento sem acionar a busca externa.

## 7. Fluxos de Conversação, Decisão e Fallback Rascunho

### 7.1 Pipeline de Processamento da Mensagem

1. **Entrada de dados:** o usuário envia uma mensagem pela interface web (`static/chat.js`), recebida pelo endpoint `POST /api/chat` em `app/main.py`.
2. **Normalização:** o texto passa por conversão de caixa, remoção de acentos e pontuação em `nlp/preprocessing.py`.
3. **Interpretação de intenção:** a CAPITU combina a similaridade de vetores TF-IDF com regras explícitas de alta precisão e uma política de limiar, margem e fora do escopo. Esse mecanismo local decide se a intenção pode ser aceita, esclarecida ou recusada; a Open Library não é usada para classificar a intenção.
4. **Extração de entidades:** o módulo `nlp/entity_extraction.py` isola os termos de busca, como título, autor ou assunto.
5. **Política, diálogo e contexto mínimo:** os módulos em `dialogue/` verificam se há parâmetro suficiente, pedem esclarecimento quando necessário, mantêm apenas o contexto de sessão necessário à seleção e resolvem referências como "o segundo".
6. **Consulta de serviço:** somente uma intenção aceita e com parâmetros suficientes é enviada a `services/open_library.py`. O adaptador consulta a Open Library, trata indisponibilidade da fonte e normaliza os resultados.
7. **Formatação da resposta:** o módulo `responses/templates.py` constrói a mensagem final, o estado da conversa e a lista de resultados exibidos no chat.

### 7.2 Regras de Esclarecimento e Fallback

* **Parâmetro ausente ou ambiguidade (`awaiting_clarification`):** quando falta título, autor ou assunto, ou quando a interpretação não é suficientemente segura, a CAPITU solicita esclarecimento e não consulta a fonte.
* **Múltiplos candidatos (`awaiting_selection`):** quando o detalhe solicitado possui mais de um candidato, a CAPITU preserva a lista da sessão e pede que a pessoa selecione uma opção; não escolhe automaticamente o primeiro resultado.
* **Busca sem resultado (`no_results`):** quando a Open Library responde sem correspondências, a CAPITU informa que não encontrou resultados naquela fonte e orienta o refinamento da busca. Isso não afirma que a obra inexiste.
* **Fora do escopo (`out_of_scope`):** perguntas sobre empréstimo, reservas, multas, disponibilidade física ou temas não bibliográficos recebem uma abstenção explicativa, sem chamada à Open Library.
* **Fonte indisponível (`source_unavailable`):** timeout, erro de rede, limite ou indisponibilidade da Open Library são informados como falha externa e são distintos de uma busca vazia.

## Referências de Trabalho

1. UNISUL. *A3 Projeto Integrador de Inteligência Artificial: desenvolvimento de um chatbot para uma demanda real de mercado*. Enunciado oficial da atividade, 2026.
2. Equipe CAPITU. [Planejamento detalhado da equipe](../CAPITU_Planejamento_Detalhado_Equipe.md). Decisões de escopo, intenções, arquitetura e limites do projeto.
3. Equipe CAPITU. [Contrato de chat v1](../contracts/chat-v1.md). Endpoint, estados de resposta, contexto mínimo e regras de fallback.
4. Equipe CAPITU. [Evidência E09](../evidence/E09.md). Composição integrada e comportamentos ponta a ponta do backend.
5. Open Library. [Developer Center](https://openlibrary.org/developers/api). Documentação da fonte pública externa de metadados bibliográficos.
