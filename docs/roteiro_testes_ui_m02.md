# Roteiro e Registro de Testes Manuais de UI (Task M02)

**Responsável:** Millena  
**Data:** Outubro de 2026  
**Ambiente:** Navegador Web (Local / Backend Simulado - Task E02)

## 1. Descrição e Objetivo
Validação visual e funcional dos fluxos básicos da interface do chatbot Capitu.IA, cobrindo os critérios de aceite UI-01 a UI-04 a partir da estrutura criada em `static/` (`index.html`, `styles.css`, `chat.js` e assets visuais em `static/images/`).

---

## 2. Elementos de Design e Identidade Visual Implementados
- **Paleta de Cores:** Identidade visual baseada na tonalidade vermelha escuro `#751b1d` (aplicada a botões, avatares, balões do usuário e destaques de status).
- **Contraste e Baloes de Mensagem:** Respostas da Capitu (IA) estilizadas com balões brancos (`#ffffff`), borda leve e sombra suave (`box-shadow`), garantindo legibilidade total sobre a imagem de fundo.
- **Estrutura de Layout:** Barra lateral (`sidebar`) com fundo claro (`#ffffff`), botão de "Nova conversa" em destaque e cartão informativo de rodapé ("Sobre esta versão") em tom suave (`#fdf2f2`).
- **Assets Visuais:** Logótipo oficial sem fundo (`Capitu.ia-Logo.png`) e imagem decorativa de acervo ao fundo do histórico do chat (`Fundo-Chat.png`).
- **Responsividade Mobile:** Adicionada regra `@media (max-width: 768px)` para adaptação em telemóveis e ecrãs pequenos, organizando o layout em coluna, ajustando espaçamentos e aumentando a largura dos balões para 90%.

---

## 3. Tabela de Validação dos Casos de Teste

| ID | Comportamento Coberto | Ação / Sequência Executada | Comportamento Esperado | Resultado Obtido | Situação |
|---|---|---|---|---|---|
| **UI-01** | Enviar mensagem válida | Digitar "Encontre o livro Torto Arado" e clicar em Enviar (ou Enter). | A mensagem do usuário é adicionada no balão vermelho `#751b1d` e a resposta da Capitu surge em balão branco sob o avatar "C". | Mensagem do usuário alinhada à direita em `#751b1d` e resposta legível em balão destacado. | **Passou** |
| **UI-02** | Entrada vazia / espaços | Tentar enviar com o campo de texto em branco ou contendo apenas espaços. | O envio é bloqueado, nenhuma mensagem é adicionada e o container do input exibe borda vermelha temporária. | Animação de erro com borda `#dc3545` por 400ms sem alteração no histórico. | **Passou** |
| **UI-03** | Estado de carregamento | Enviar mensagem e observar o intervalo de resposta simulado. | Exibir indicador "Consultando acervo..." durante o tempo de espera, sendo removido ao chegar a resposta. | Elemento temporário exibido e removido após o delay simulado de 1.2s. | **Passou** |
| **UI-04** | Exibição de múltiplos resultados | Digitar "Quais são as obras de Machado de Assis?". | Apresentar resposta da Capitu acompanhada dos cards numerados de obras ("01 Dom Casmurro", "02 Memórias Póstumas..."). | Cards estilizados renderizados corretamente dentro do balão da Capitu sem quebrar o layout. | **Passou** |
| **UI-05** | Layout Responsivo (Mobile) | Redimensionar a janela do navegador para <= 768px ou usar o simulador mobile do DevTools (F12). | O layout adapta-se verticalmente, oculta o menu secundário da sidebar e ajusta os balões e o input ao ecrã reduzido. | Interface responsiva sem barra de rolagem horizontal e mantendo total legibilidade e funcionalidade. | **Passou** |

---

## 4. Conclusão e Autoria
Os testes manuais confirmaram a conformidade da interface com o protótipo do Figma e com o contrato de mensagens. A estrutura modular em `static/` está pronta para ser conectada ao backend real na Task M03.