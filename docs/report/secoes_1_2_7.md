# Relatório Técnico CAPITU — Seções 1, 2 e Rascunho da 7

## 1. Problema, Público-Alvo e Objetivos

### 1.1 Definição do Problema
Estudantes e pesquisadores acadêmicos frequentemente iniciam buscas por material bibliográfico com dados parciais ou descrições em linguagem natural (ex.: "livro sobre inteligência artificial", "obras de Machado de Assis"). Os sistemas de catálogo de biblioteca tradicionais exigem buscas parametrizadas exatas e títulos precisos, gerando alta taxa de insucesso na localização inicial de obras. A CAPITU atua em um cenário simulado de biblioteca universitária para intermediar a interpretação de dúvidas bibliográficas em linguagem natural.

### 1.2 Público-Alvo
* **Usuários Primários**: Estudantes de graduação, pós-graduação e pesquisadores acadêmicos.
* **Necessidades**: Descoberta rápida de obras por tema, identificação da bibliografia de um autor e consulta a detalhes de livros a partir de requisições informais em português.

### 1.3 Objetivos do Sistema
* **Objetivo Geral**: Processar solicitações bibliográficas informais, classificar a intenção do usuário, extrair entidades relevantes e recuperar metadados confiáveis via Open Library.
* **Objetivos Específicos**:
  1. Mapear as requisições em quatro intenções operacionais consistentes.
  2. Extrair parâmetros de busca (título, autor, assunto).
  3. Realizar perguntas de esclarecimento em caso de ambiguidade ou parâmetros ausentes.
  4. Garantir que o sistema não alegue acervo físico ou dados bibliográficos sem evidências provenientes da API externa.

---

## 2. Escopo, Intenções e Limitações do Domínio

### 2.1 Escopo de Atuação
O sistema cobre exclusivamente a descoberta de obras e consulta de metadados bibliográficos em fontes públicas abertas.

### 2.2 As Quatro Intenções Consistentes

| Intenção | Descrição | Exemplo de Requisição |
| :--- | :--- | :--- |
| `buscar_por_titulo` | Busca de obras pelo título parcial ou completo | "Procure o livro Dom Casmurro" |
| `buscar_obras_autor` | Mapeamento das obras publicadas por um autor | "Quais livros Machado de Assis escreveu?" |
| `buscar_por_assunto` | Localização de livros por tema, assunto ou gênero | "Quero livros sobre inteligência artificial" |
| `consultar_detalhes` | Obtenção de metadados específicos de uma obra identificada | "Quem escreveu o livro O Alienista?" |

### 2.3 Limitações Explícitas do Domínio
* **Gestão Física Ausente**: O sistema não informa disponibilidade em estante, localização física, empréstimos, renovações ou multas.
* **Evidência Obrigatória**: O sistema limita-se aos dados retornados pela Open Library. Nenhum resultado ou catálogo é inventado.
* **Abstenção por Baixa Confiança**: Requisições fora do escopo ou com score de similaridade TF-IDF abaixo do limiar congelado disparam mensagens de abstenção ou esclarecimento sem acionar a busca externa.

---

## 7. Fluxos de Conversação, Decisão e Fallback (Rascunho)

### 7.1 Pipeline de Processamento da Mensagem
1. **Entrada de Dados**: O usuário envia uma mensagem pela interface web (`chat.js`), recebida pelo endpoint `/chat` em `app/main.py`.
2. **Normalização**: O texto passa por conversão de caixa, remoção de acentos e pontuação em `nlp/preprocessing.py`.
3. **Classificação de Intenção**: O módulo `nlp/intent_similarity.py` calcula a similaridade do vetor TF-IDF em relação ao corpus de intenções.
4. **Extração de Entidades**: O módulo `nlp/entity_extraction.py` isola os termos de busca (título, autor ou assunto).
5. **Consulta de Serviço**: O serviço `services/open_library.py` efetua a busca na API externa.
6. **Formatação da Resposta**: O módulo `responses/templates.py` constrói a mensagem final exibida no chat.

### 7.2 Regras de Esclarecimento e Fallback
* **Parâmetro Ausente**: Quando a intenção é identificada, mas a entidade necessária está ausente (ex.: "Busque um livro"), a CAPITU solicita a informação faltante antes de consultar a API.
* **Fora do Escopo / Baixa Confiança**: Quando o score de similaridade fica abaixo do limiar de decisão ou a requisição envolve operações institucionais (ex.: "Renove meu empréstimo"), o sistema dispara abstenção informativa.