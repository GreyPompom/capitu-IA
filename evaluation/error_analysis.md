# Análise de erros

Registrar no mínimo três falhas observadas, com entrada, estado, esperado/obtido, camada provável, impacto, correção e teste de regressão. Não inventar resultados.

## REG-001 - Título não extraído em pedido de resumo

| Campo | Registro |
| --- | --- |
| Data da observação | 11/11/2026 |
| Entrada | `quero ler o livro O pequeno principe, me de um resumo` |
| Estado inicial | Nova conversa, sem contexto ou seleção anterior. |
| Intenção esperada | `consultar_detalhes` |
| Entidades esperadas | `title = O pequeno principe`; `requested_field = description`. |
| Comportamento esperado | Buscar detalhes da obra em fonte controlada e apresentar a descrição disponível; se a fonte não a fornecer, informar essa ausência sem inventar resumo. |
| Resultado obtido | A mensagem foi reconhecida como `consultar_detalhes` e `description`, porém o extrator devolveu `title = None`. O diálogo retornou `awaiting_clarification` com a pergunta pelo título. |
| Camada provável | Extração de entidades em `nlp/entity_extraction.py`. Os padrões de detalhe não cobrem a formulação “quero ler o livro [título], me dê um resumo”. |
| Evidência | Captura da UI fornecida por Emely e diagnóstico local de `extract_entities` em 11/11/2026. Não houve chamada à Open Library porque o parâmetro obrigatório não foi extraído. |
| Impacto | Alto para a usabilidade do fluxo de detalhes: uma solicitação em linguagem natural dentro do escopo exige repetição desnecessária do título. |
| Correção proposta | Adicionar um padrão específico que preserve o trecho entre “livro” e a solicitação de resumo/descrição, sem alterar o tratamento de referências contextuais. |
| Teste de regressão necessário | Criar teste unitário em `tests/test_entity_extraction.py` para confirmar título e `requested_field = description`; criar teste de integração com catálogo fake para confirmar que a consulta ocorre e a descrição controlada é exibida. |
| Situação | Aberta - não corrigida. |
