# Registro de Validação em Dupla (Revisão Cega)

**Avaliadora de Criação:** Millena
**Avaliador Cego (Revisor):** Miguel

Conforme exigido pelos Critérios de Aceite (GATE-B) e pelas regras de sincronização da Task M01, este documento registra a amostra de frases criadas e submetidas a uma validação cega. O revisor não teve acesso aos rótulos originais para classificar a intenção e identificar possíveis duplicatas.

### Amostra Avaliada e Resultados

| ID | Texto da Amostra | Rótulo Original (Millena) | Classificação do Revisor (Miguel) | Resultado / Divergência | Duplicata Estrutural? |
|---|---|---|---|---|---|
| A01 | Você encontra Dom Casmurro? | buscar_por_titulo | O usuário quer que eu busque pelo título "Dom Casmurro" na base. | **Concordância.** (buscar_por_titulo) | Não. |
| A02 | Quais livros Machado de Assis escreveu? | buscar_obras_autor | O usuário quer que eu busque quais títulos são associados ao autor "Machado de Assis". | **Concordância.** (buscar_obras_autor) | Não. |
| A03 | Mostre livros de ficção científica. | buscar_por_assunto | O usuário quer q eu busque títulos associados ao assunto "Ficção Científica". | **Concordância.** (buscar_por_assunto) | Não. |
| A04 | Qual é o ano dessa edição? | consultar_detalhes | O usuário gostaria de verificar o ano de lançamento de um título não informado. | **Concordância.** (consultar_detalhes, obra implícita). | Não. |
| A05 | Busca pra mim O Senhor dos Anéis | buscar_por_titulo | O usuário quer q eu achei o título "Senhor dos anéis". | **Concordância.** (buscar_por_titulo) | Parcial. Mesma intenção de A01, mas formato verbal diferente. |

### Conclusão da Revisão
A amostra confirmou que as frases criadas são representativas e as classes bem delimitadas. O revisor conseguiu identificar perfeitamente as entidades alvo (Autor, Título, Assunto) e inferir os campos desejados (ano de lançamento). Não houve divergência de intenções que justifique fusão ou separação de categorias neste momento inicial. A base de dados principal (`intents.csv`) foi atualizada para indicar os agrupamentos de variação e a origem das frases.