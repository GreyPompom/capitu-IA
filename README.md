# CAPITU IA

Chatbot inteligente de descoberta bibliográfica para a atividade A3 de Inteligência Artificial. O backend FastAPI expõe o contrato do chat, integra interpretação TF-IDF/regras, contexto de conversa e a Open Library como fonte externa de dados.

## Documentação

Consulte [`docs/README.md`](docs/README.md) para os documentos de planejamento e a regra de sincronização PDF/Markdown.

## Estrutura

- `app/`: interface HTTP e schemas.
- `nlp/`: pré-processamento, similaridade TF-IDF e entidades.
- `dialogue/`: contexto, política e orquestração.
- `services/`: Open Library, normalização e cache opcional.
- `responses/` e `static/`: respostas e chat web local.
- `data/`, `artifacts/`, `evaluation/` e `tests/`: dados, avaliações e testes.
- `docs/`: requisitos, arquitetura, planejamento e evidências.

## Funcionalidades e limites atuais

Planejamento aprovado pelo professor. A CAPITU interpreta quatro intenções bibliográficas: busca por título, obras de autor,
busca por assunto/gênero e consulta de detalhes. A interpretação combina
normalização, TF-IDF/similaridade, regras de alta precisão, extração de
entidades e contexto mínimo da conversa. Os dados bibliográficos vêm da Open
Library.

O sistema trata ambiguidade, ausência de parâmetro, resultado vazio, pergunta
fora de escopo e indisponibilidade da fonte. A interface cancela uma requisição
de chat que ultrapasse 15 segundos e permite nova tentativa.

Limites intencionais: a CAPITU não realiza empréstimos, reservas, consulta a
acervo institucional ou respostas interpretativas sobre personagens/enredo.
Resultados da Open Library podem variar e uma busca vazia não comprova que uma
obra não exista.

## Executar localmente

Requisitos:

- Python 3.10 ou superior;
- `pip` disponível no Python escolhido;
- conexão com a internet apenas para consultas reais à Open Library;
- navegador moderno para a interface web.

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -e ".[dev]"
.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload
```

Abra `http://127.0.0.1:8000/`. A documentação HTTP fica em `http://127.0.0.1:8000/docs`.

Se a porta 8000 estiver ocupada, use outra porta, por exemplo:

```powershell
.\.venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8766
```

Nesse caso, abra `http://127.0.0.1:8766/`.

## Validar o projeto

```powershell
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe scripts\build_index.py
.\.venv\Scripts\python.exe scripts\run_g05_acceptance.py --mode fixture
.\.venv\Scripts\python.exe scripts\run_g06_reproduction.py --repeats 3
```

`build_index.py` ajusta o índice somente com `data/splits/reference.csv` e cria
artefatos locais em `artifacts/`; os arquivos gerados não são versionados. Os
casos controlados não dependem de rede. Evidências, métricas e limitações estão
em [`docs/evidence/`](docs/evidence/) e [`evaluation/`](evaluation/).
