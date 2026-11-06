# CAPITU IA

Chatbot inteligente de descoberta bibliográfica para a atividade A3 de Inteligência Artificial. O backend FastAPI valida o contrato E01 e disponibiliza uma resposta demonstrativa local; o índice TF-IDF de intenções da E04 está implementado, mas ainda será integrado ao fluxo de diálogo e à Open Library nas próximas tarefas.

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

## Estado

Planejamento aprovado pelo professor conforme informado pela equipe. E01 define o contrato v1 e os schemas Pydantic. E02 entrega o servidor local, `POST /api/chat`, página estática-base e testes HTTP. E03 curou o corpus e separou referência, validação e teste sem vazamento. E04 implementa normalização, TF-IDF e similaridade cosseno. E05 adiciona política de limiar, ambiguidade e fora de escopo. E06 extrai parâmetros; E07 mantém contexto mínimo; E08 implementa cliente e normalização da Open Library. E09 integra essas camadas no endpoint para as quatro intenções. E10 adiciona cache TTL, ritmo compartilhado e uma única retentativa controlada para falhas transitórias da fonte.

## Executar localmente

Requer Python 3.10 ou superior.

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -e ".[dev]"
.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload
```

Abra `http://127.0.0.1:8000/`. A documentação HTTP fica em `http://127.0.0.1:8000/docs`.

Para validar o projeto, execute `.\.venv\Scripts\python.exe -m pytest -q`.
