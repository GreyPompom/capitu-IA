"""Backend HTTP da CAPITU: contrato, PLN, diálogo e fonte bibliográfica."""

from pathlib import Path
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.chat_service import CapituChatService
from app.schemas import ChatRequest, ChatResponse


PROJECT_ROOT = Path(__file__).resolve().parents[1]
STATIC_DIR = PROJECT_ROOT / "static"

app = FastAPI(
    title="CAPITU",
    description="Chatbot local de descoberta bibliográfica. Resposta de demonstração E02.",
    version="0.1.0",
)

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
chat_service = CapituChatService()


@app.get("/", include_in_schema=False)
def serve_chat() -> FileResponse:
    """Serve a página-base na mesma origem da API."""

    return FileResponse(STATIC_DIR / "index.html", media_type="text/html")


@app.post("/api/chat", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:
    """Processa uma mensagem válida usando o fluxo integrado da CAPITU."""

    return chat_service.handle(request)
