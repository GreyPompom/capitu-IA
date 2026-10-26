# Roteiro e Registro de Testes Manuais de UI (Task M02)

**Responsável:** Millena  
**Data:** Outubro de 2026  
**Ambiente:** Navegador Web (Servido via FastAPI `/` e `/static/` - Conexão com `POST /api/chat`)

## 1. Descrição e Objetivo
Validação visual e funcional dos fluxos básicos da interface do chatbot Capitu.IA, conectada ao endpoint `POST /api/chat` (Task E02), cobrindo o envio de `message` e `session_id`, bloqueio de duplo envio, segurança contra injeção de HTML, ações da barra lateral e renderização dos estados da API.

---

## 2. Elementos de Design e Identidade Visual Implementados
- **Paleta de Cores:** Identidade visual baseada na tonalidade vermelha escuro `#751b1d` (aplicada a botões, avatares, balões do usuário e destaques de status).
- **Contraste e Baloes de Mensagem:** Respostas da Capitu (IA) estilizadas com balões brancos (`#ffffff`), borda leve e sombra suave (`box-shadow`), garantindo legibilidade total sobre a imagem de fundo.
- **Estrutura de Layout:** Barra lateral (`sidebar`) com fundo claro (`#ffffff`), botão de "Nova conversa" em destaque e cartão informativo de rodapé ("Sobre esta versão") em tom suave (`#fdf2f2`).
- **Assets Visuais:** Logótipo oficial sem fundo (`Capitu.ia-Logo.png`) e imagem decorativa de acervo ao fundo do histórico do chat (`Fundo-Chat.png`).
- **Responsividade Mobile:** Adicionada regra `@media (max-width: 768px)` para adaptação em telemóveis e ecrãs pequenos, organizando o layout em coluna, ajustando espaçamentos e aumentando a largura dos balões para 90%.
- **Conexão com Backend:** Envio de requisições `POST /api/chat` via `fetch` assíncrono com cabeçalho `Content-Type: application/json` e payload contendo `message` e `session_id`.
- **Prevenção contra Injeção de HTML (XSS):** Todo conteúdo textual do usuário e das respostas é inserido via `textContent` e construção manual de nós DOM (`createElement`), impedindo execução de marcas HTML maliciosas.
- **Prevenção de Envio Duplicado:** O botão de envio e o campo de texto permanecem desabilitados (`disabled`) enquanto a requisição aguarda o retorno do servidor.
- **Roteamento de Arquivos Estáticos:** Compatibilidade com o FastAPI através dos caminhos absolutos prefixados com `/static/`.
- **Controles da Sidebar e Cards:** Botão "Nova conversa" reinicia a sessão (`session_id`), atalhos preenchem o input e cliques em cards de livros iniciam consulta de detalhes.

---

## 3. Tabela de Validação dos Casos de Teste

| ID | Comportamento Coberto | Ação / Sequência Executada | Comportamento Esperado | Resultado Obtido | Situação |
|---|---|---|---|---|---|
| **UI-01** | Envio válido via `POST /api/chat` | Digitar "Encontre livros de Machado de Assis" e enviar. | Requisição enviada com `message` e `session_id`. Resposta e cards do backend renderizados em balão destacado. | Dados retornados da API exibidos corretamente sem uso de `innerHTML`. | **Passou** |
| **UI-02** | Entrada vazia / espaços | Tentar enviar mensagem com input em branco. | Envio bloqueado, borda vermelha temporária de erro exibida e nenhuma requisição disparada. | Animação de erro em 400ms sem disparo de rede. | **Passou** |
| **UI-03** | Estado de carregamento e Bloqueio de Envio Duplicado | Enviar mensagem e tentar clicar em Enviar ou teclar Enter durante a busca. | Exibir "Consultando acervo..." e manter input/botão desabilitados (`disabled`) até o fim da requisição. | Envio duplo impedido com sucesso; controles reabilitados no bloco `finally`. | **Passou** |
| **UI-04** | Exibição de Lista Múltipla, Vazia e Única | Enviar consultas retornando 0, 1 ou múltiplos resultados do backend. | Se houver lista, renderizar cards clicáveis. Se for vazia, exibir mensagem informativa do backend. | Todos os estados de lista processados com estrutura DOM segura. | **Passou** |
| **UI-05** | Ações da Sidebar e Reinício de Sessão | Clicar em "Nova conversa" e nos atalhos do menu ("Buscar por título", etc.). | "Nova conversa" gera novo `session_id` e limpa o chat. Atalhos preenchem o input com o prefixo correspondente. | Histórico resetado e campo de entrada preenchido ao clicar nos itens. | **Passou** |
| **UI-06** | Clique em Card de Resultado | Clicar em um card de livro retornado em uma busca. | O título do livro é preenchido no input com comando "Consultar detalhes" e a busca é disparada automaticamente. | Consulta de detalhes executada com sucesso ao clicar no card. | **Passou** |
| **UI-07** | Layout Responsivo (Mobile) | Redimensionar janela para <= 768px. | Interface adapta-se verticalmente mantendo legibilidade e acessibilidade dos botões. | Layout fluido ajustado sem estouro de rolagem horizontal. | **Passou** |

---

## 4. Conclusão e Autoria
A interface em `static/` encontra-se 100% integrada com a API `POST /api/chat` conforme o contrato `docs/contracts/chat-v1.md`, cumprindo todos os requisitos funcionais, estáticos e de segurança da Task M02.