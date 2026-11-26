# Relatório Técnico CAPITU — Seções 4, 5 e 6

> Texto-fonte técnico da E14. Para a versão entregue em DOCX/PDF, manter as
> referências, denominadores e limitações aqui declarados.

## 4. Arquitetura da Solução

### 4.1 Visão geral

A CAPITU é um chatbot local de descoberta bibliográfica. A pessoa usuária
interage com uma interface web simples; a mensagem é enviada ao endpoint
`POST /api/chat` do backend FastAPI. O backend interpreta a mensagem, mantém
o contexto mínimo da sessão, consulta a Open Library quando necessário e
retorna texto, estado conversacional, intenção e até cinco resultados. A Open
Library é exclusivamente a fonte externa de metadados: ela não classifica a
intenção e não constitui, por si só, o mecanismo de Inteligência Artificial.

```text
Usuário → chat web → FastAPI → normalização
        → TF-IDF + regras + política → extração de entidades
        → diálogo/contexto → Open Library → normalização de dados
        → resposta estruturada → chat web
```

As responsabilidades foram separadas para reduzir acoplamento: `app/` contém
o contrato HTTP e a orquestração; `nlp/` contém pré-processamento, índice e
extração; `dialogue/` controla estados e contexto; `services/` encapsula a
Open Library, cache e normalização; `responses/` constrói mensagens
determinísticas; e `static/` contém a interface HTML, CSS e JavaScript. Essa
divisão permite testar o serviço de conversa com um catálogo controlado, sem
rede, e evita regras de negócio diretamente na rota HTTP.

### 4.2 Contrato e estados

O contrato versão 1 recebe `message` (1 a 1.000 caracteres) e, opcionalmente,
`session_id`. A resposta contém `session_id`, `text`, `state`, `intent` e
`results`. Os estados distinguem resposta normal (`answered`), solicitação de
complemento (`awaiting_clarification`), escolha entre candidatos
(`awaiting_selection`), busca vazia (`no_results`), pergunta fora do escopo
(`out_of_scope`) e indisponibilidade da fonte (`source_unavailable`).

Essa distinção é importante: a ausência de resultados na Open Library não
autoriza afirmar que uma obra não existe; falha de rede também não deve ser
apresentada como lista vazia. Em caso de múltiplos resultados para uma consulta
de detalhes, a CAPITU não seleciona o primeiro automaticamente. Ela mantém os
candidatos da sessão e aceita referências como “o segundo”.

O contexto não armazena histórico permanente nem dados pessoais. Ele conserva
somente o identificador da sessão, o estado, a intenção/parâmetro pendente, os
últimos resultados e, quando houver, a obra selecionada. Assim, uma pergunta
posterior como “qual autor?” pode ser respondida sobre a obra escolhida sem
nova busca por título.

### 4.3 Integração e resiliência da fonte externa

O adaptador da Open Library consulta por título, autoria, assunto e chave de
obra. Ele solicita apenas campos úteis ao MVP, normaliza campos ausentes para
`null` ou listas vazias e limita a lista a cinco resultados. O serviço usa
cache TTL em memória, espaçamento entre chamadas e no máximo uma retentativa
para timeout, erro de rede, HTTP 429 e erros 5xx. O `Retry-After` só é usado
quando o prazo é válido e não superior a cinco segundos. Erros 4xx não
transitórios e JSON inválido não são repetidos.

A interface possui também timeout de 15 segundos para uma requisição de chat.
Ao excedê-lo, a página cancela a chamada, informa a possibilidade de nova
tentativa e libera seus controles. Esse tratamento é complementar ao do
backend: a fonte pode estar indisponível e a interface não deve permanecer em
carregamento indefinidamente.

## 5. Implementação da Inteligência Artificial e do PLN

### 5.1 Dados, representação e classificação

O mecanismo local foi implementado pela equipe com scikit-learn. O corpus é
curado e dividido em `reference.csv`, `validation.csv` e `test.csv`. O índice
é ajustado **somente** com os 84 exemplos de referência; validação e teste não
participam do vocabulário TF-IDF. A separação evita que exemplos reservados
sejam incorporados diretamente ao modelo. Cada frase recebe normalização de
Unicode, caixa, acentos, pontuação e espaços. Em seguida, um
`TfidfVectorizer` usa unigramas e bigramas com normalização L2 e TF
sublinear.

Para uma nova mensagem, a CAPITU calcula a similaridade cosseno entre o vetor
da mensagem e cada exemplo de referência. Em vez de decidir por uma única
frase mais próxima, ela agrupa os resultados por intenção e calcula a média dos
três maiores cossenos de cada classe. As quatro classes de negócio são
`buscar_por_titulo`, `buscar_obras_autor`, `buscar_por_assunto` e
`consultar_detalhes`.

O score resultante é uma **similaridade cosseno**, não uma probabilidade
calibrada. Ele é usado apenas como evidência para a política de decisão e não
como afirmação de certeza estatística ao usuário.

### 5.2 Política híbrida e limiares

A solução final é híbrida. O ranking TF-IDF oferece generalização lexical para
frases semelhantes às referências; regras de alta precisão reconhecem comandos
claros, como “quem escreveu”, “liste obras de” e “livros sobre”; e a política
de decisão impede que o sistema consulte a fonte diante de sinais insuficientes
ou fora do domínio. A precedência é:

1. operação fora do escopo;
2. ambiguidade conhecida ou referência curta sem ação;
3. ausência de evidência;
4. limiar de similaridade;
5. margem entre os dois melhores candidatos;
6. aceite da intenção.

Na calibração anterior à avaliação, a média dos três melhores exemplos teve
7/18 acertos top-1 brutos, contra 6/18 do vizinho mais próximo. Foi adotado o
limiar `τ = 0,25` e a margem `δ = 0,12`. Entre os valores testados, `0,25`
preservou os dois aceites corretos observados sem falso aceite na validação; a
margem pede esclarecimento quando as duas intenções mais plausíveis ficam muito
próximas. Regras estritas podem aceitar comandos inequívocos mesmo com score
baixo; nesses casos o score é apenas diagnóstico e a margem não é aplicada.

Como alternativa, regras puras seriam simples de explicar, mas exigiriam
cobertura manual de muitas reformulações. O vizinho mais próximo foi testado e
teve desempenho bruto inferior no conjunto de validação. Uma arquitetura com
LLM generativo não foi escolhida porque aumentaria custo, dependência externa
e dificuldade de demonstrar a técnica própria de PLN, além de extrapolar o
MVP. A abordagem híbrida preserva um algoritmo identificável, testável e
compatível com o escopo.

### 5.3 Entidades e diálogo

Depois da intenção, regras de extração identificam título, autor, assunto,
ISBN e, na consulta de detalhes, o campo solicitado (`author`,
`first_publish_year`, `isbn`, `publisher`, `description`, `subjects` ou
`edition_count`). A extração preserva o trecho original informado pelo usuário
para que a consulta não perca caixa ou acentos. Quando falta o parâmetro
principal, ou há conflito entre autor e assunto, a política de diálogo pede
esclarecimento em vez de enviar texto arbitrário à API.

O mecanismo não responde perguntas interpretativas de enredo ou personagens.
Quando uma mensagem pede resumo e também traz esse tipo de pergunta, a CAPITU
retorna apenas a descrição disponível da obra e informa explicitamente seu
limite. Do mesmo modo, não afirma disponibilidade física, empréstimo, reserva,
renovação, multa ou consulta a acervo institucional.

## 6. Avaliação, Resultados e Análise Crítica

### 6.1 Estratégia de avaliação

A avaliação separa qualidade de interpretação, comportamento conversacional e
integração com a fonte externa. O avaliador E11 ajusta o índice apenas com a
referência e executa os 18 casos de `test.csv` sem rede. Ele registra hashes
dos arquivos, previsões, matriz de confusão e denominadores. As métricas de
intenção são accuracy, precision, recall, F1 macro e menor F1 por intenção; a
taxa de fallback mede rejeições ou esclarecimentos no mesmo denominador. Para
entidades e campos solicitados, usa-se acerto exato.

Os roteiros G05 e G06 complementam a avaliação com catálogo controlado. G05
verifica 24 cenários funcionais sem rede, incluindo resultados vazios,
ambiguidade, seleção e falha externa simulada. G06 repete sete cenários três
vezes para verificar determinismo da interpretação e das chamadas ao catálogo.
Esses roteiros não medem a qualidade variável da Open Library ao vivo; medem
se a CAPITU executa o fluxo previsto quando a fonte é controlada.

### 6.2 Resultados de regressão E11

Na execução pós-correção de 16/11/2026, os 18 casos do teste registraram 16
decisões corretas. A tabela apresenta a métrica completa, incluindo dois casos
que dependem de contexto prévio da sessão.

| Medida | Resultado |
| --- | ---: |
| Accuracy geral | 88,89% (16/18) |
| Macro precision | 100,00% |
| Macro recall | 87,50% |
| Macro F1 | 92,86% |
| Menor F1 por intenção | 85,71% |
| Fallback/abstenção | 11,11% (2/18) |
| Entidade principal | 100,00% (16/16) |
| Campo solicitado | 100,00% (4/4) |
| Negativos e ambíguos G02 | 100,00% (20/20) |

A meta interna da equipe foi no mínimo 75% para métricas que devem crescer e,
para fallback, no máximo 25%. Esses valores foram atingidos na regressão. A
matriz de confusão completa teve cinco acertos de título, três de autoria e um
fallback, cinco de assunto e três de detalhes e um fallback. Não houve troca
direta de uma intenção positiva por outra; os dois erros foram abstenções.

No recorte diagnóstico de 16 mensagens independentes, removendo dois casos que
dependem de um turno anterior, a accuracy foi 93,75% (15/16) e o Macro F1 foi
96,43%. Esse recorte não substitui a métrica completa: ele apenas isola o
classificador da dependência de contexto.

No comportamento funcional, a última execução controlada de G05 obteve 24/24
cenários aprovados; G06 obteve 7/7 cenários aprovados em três repetições, sem
divergência. Também foram executadas 52 regressões direcionadas de PLN,
contexto, construção do índice e contrato estático da interface. A execução
HTTP de `TestClient` e o smoke por soquete local devem ser repetidos fora do
executor automatizado, que bloqueou soquetes locais; esse limite operacional
foi registrado na E13 e não é apresentado como teste aprovado.

### 6.3 Falhas observadas e correções

Três falhas reais foram preservadas para análise. Primeiro, a formulação
“Estou atrás de um livro chamado 1984” era rejeitada porque não tinha regra de
alta precisão nem padrão de extração; foram adicionados padrão de título e
teste de regressão. Segundo, “Me mostre ficção científica” enviava o comando
inteiro como assunto; a extração passou a isolar somente “ficção científica”.
Terceiro, uma requisição web sem resposta deixava a interface em carregamento
permanente; foi implementado timeout de 15 segundos com cancelamento e
liberação dos controles.

As duas primeiras falhas passaram 3/3 na reprodução controlada G06 e são
cobertas por testes de entidade e integração. A terceira possui evidência
visual histórica e teste estático que verifica a presença do cancelamento,
limite, mensagem e limpeza. A confirmação visual do timeout no navegador deve
ser mantida como evidência operacional, não convertida em métrica de PLN.

### 6.4 Limitações e ameaças à validade

O conjunto `test.csv` foi examinado durante a análise das falhas e orientou
correções. Portanto, 88,89% e 92,86% comprovam uma **regressão de
desenvolvimento** nos cenários conhecidos, e não uma estimativa independente
definitiva de generalização. Uma validação cega com perguntas inéditas,
elaboradas por integrante que não altere regras nem veja previsões, é a forma
adequada de fortalecer essa evidência antes da apresentação.

Além disso, resultados da Open Library podem mudar, faltar ou ficar
indisponíveis. A CAPITU trata essas situações, mas não garante que toda obra
exista na fonte, que seus metadados sejam completos ou que uma busca ao vivo
repita exatamente a lista anterior. O sistema também não fornece respostas
interpretativas sobre obras, recomendações personalizadas nem serviços de uma
biblioteca física. Esses limites devem ser apresentados na demonstração e no
relatório, pois fazem parte do escopo responsável do protótipo.

## Referências e evidências técnicas

1. Equipe CAPITU. [`architecture.md`](../architecture.md). Componentes e
   contrato executável.
2. Equipe CAPITU. [`E04.md`](../evidence/E04.md) e [`E05.md`](../evidence/E05.md).
   Índice TF-IDF, comparação de agregação, limiar e margem.
3. Equipe CAPITU. [`E09.md`](../evidence/E09.md) e [`E10.md`](../evidence/E10.md).
   Integração, normalização, cache, retentativa e limites da fonte.
4. Equipe CAPITU. [`e11_summary.md`](../../evaluation/results/e11_summary.md) e
   [`e11_intent_metrics.json`](../../evaluation/results/e11_intent_metrics.json).
   Métricas, matriz e denominadores.
5. Equipe CAPITU. [`error_analysis.md`](../../evaluation/error_analysis.md) e
   [`E13.md`](../evidence/E13.md). Falhas reais e limites de reprodução.
6. Open Library. [Developer Center](https://openlibrary.org/developers/api).
   Fonte pública de metadados bibliográficos.
