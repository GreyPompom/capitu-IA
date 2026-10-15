"""Backend HTTP mínimo da CAPITU, com resposta demonstrativa para E02."""

from pathlib import Path
from uuid import uuid4

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.schemas import BookSummary, ChatRequest, ChatResponse, ConversationState


PROJECT_ROOT = Path(__file__).resolve().parents[1]
STATIC_DIR = PROJECT_ROOT / "static"

app = FastAPI(
    title="CAPITU",
    description="Chatbot local de descoberta bibliográfica. Resposta de demonstração E02.",
    version="0.1.0",
)

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.get("/", include_in_schema=False)
def serve_chat() -> FileResponse:
    """Serve a página-base na mesma origem da API."""

    return FileResponse(STATIC_DIR / "index.html", media_type="text/html")


@app.post("/api/chat", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:
    """Valida o contrato e devolve dados locais simulados, sem IA ou rede externa."""

    session_id = request.session_id or uuid4()
    demo_book = BookSummary(
        openlibrary_key="/works/OL-E02-DEMO",
        title="Livro de demonstração (dados fictícios)",
        authors=["Autoria fictícia para demonstração"],
        first_publish_year=None,
        edition_count=None,
        isbn=[],
        subjects=["simulação"],
        cover_url=None,
        source_url="https://example.org/capitu-fixtures/OL-E02-DEMO",
    )
    return ChatResponse(
        session_id=session_id,
        text=(
            "Resposta simulada da E02. A mensagem foi recebida, mas a intenção "
            "ainda não é interpretada e este registro fictício não foi consultado "
            "na Open Library."
        ),
        state=ConversationState.ANSWERED,
        intent=None,
        results=[demo_book],
    )
