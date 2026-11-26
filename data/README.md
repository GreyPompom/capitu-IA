# Dados da CAPITU

## Finalidade e origem

Os dados locais são exemplos de linguagem elaborados pelos integrantes para desenvolver e avaliar o reconhecimento de intenções da CAPITU. Os exemplos positivos de `intents.csv` são escritos pela equipe e identificados por `origem`; os casos de `Fora_Do_Escopo_Ambiguo.csv` foram preparados para testar abstenção e pedido de esclarecimento. A Open Library é consultada em tempo de execução para informações bibliográficas e não é a origem desses enunciados de treino.

## Formatos e campos

- `intents.csv`: CSV UTF-8 separado por vírgulas, com cabeçalho `id,texto,intencao,entidade,campo_solicitado,grupo_variacao,origem`. `id` identifica a amostra; `texto` é a mensagem; `intencao` é uma das quatro classes bibliográficas descritas no guia; `entidade` e `campo_solicitado` registram o parâmetro principal; `grupo_variacao` agrupa paráfrases relacionadas; `origem` registra a autoria/origem declarada.
- `Fora_Do_Escopo_Ambiguo.csv`: CSV UTF-8 separado por vírgulas, com cabeçalho `id,tipo,entrada,estado_esperado,acao_esperada,motivo`. Os exemplos negativos e ambíguos servem à avaliação do comportamento de abstenção ou esclarecimento, não devem ser incorporados automaticamente como classes positivas de treino.
- `annotation_guide.md`: definições operacionais, regras de anotação e tratamento de contexto.

## Privacidade, autorização e uso

Os exemplos são enunciados sintéticos/autoriais para fins acadêmicos. Não devem conter nomes, contatos, histórico de leitura ou qualquer outro dado pessoal de usuários reais. Os integrantes devem confirmar entre si a autoria e a autorização para manter e publicar suas contribuições no repositório acadêmico; não incluir conteúdo de terceiros sem permissão ou atribuição adequada. Não são armazenadas credenciais da API nem dados de conversas reais nestes arquivos.

## Curadoria e versionamento

Preserve IDs estáveis, registre autoria/origem, siga `annotation_guide.md` e atualize esta documentação junto com mudanças de formato ou finalidade. Agrupe paráfrases próximas antes de separar treino, validação e teste para reduzir vazamento de dados. Não mova exemplos do conjunto de avaliação para o treino sem criar versão documentada e manter uma avaliação independente.

## E03 — splits e revisão humana

Os exemplos `E03-*` em `intents.csv` são rascunhos criados com assistência de IA e aguardam validação semântica humana. Faça primeiro a anotação cega em `e03_human_validation.csv`; instruções e critérios estão em [`docs/evidence/E03_human_validation.md`](../docs/evidence/E03_human_validation.md). Não use o corpus para avaliação final antes dessa revisão.

Execute `python scripts/prepare_dataset_splits.py` para gerar `splits/reference.csv`, `splits/validation.csv`, `splits/test.csv` e `splits/manifest.json`. A separação é determinística por `grupo_variacao`, com alvo aproximado de 70/15/15. A folha humana existente é preservada quando o script é executado novamente. Somente `reference.csv` pode ser usado para ajustar o TF-IDF; reserve `test.csv` para avaliação final.
