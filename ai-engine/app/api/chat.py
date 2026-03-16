from fastapi import APIRouter

from ..models import (
    ChatRequest,
    ChatResponse,
    KnowledgeIngestRequest,
    KnowledgeIngestResponse,
    KnowledgeListResponse,
    LibraryStatusResponse,
)
from ..services.memory import ingest_knowledge, library_status, list_knowledge
from ..services.orchestrator import handle_chat

router = APIRouter()


@router.post("/respond", response_model=ChatResponse)
def respond(payload: ChatRequest) -> ChatResponse:
    return handle_chat(payload)


@router.post("/knowledge", response_model=KnowledgeIngestResponse)
def ingest(payload: KnowledgeIngestRequest) -> KnowledgeIngestResponse:
    return ingest_knowledge(payload)


@router.get("/knowledge", response_model=KnowledgeListResponse)
def knowledge(user_id: str = "demo-user") -> KnowledgeListResponse:
    return KnowledgeListResponse(items=list_knowledge(user_id))


@router.get("/library/status", response_model=LibraryStatusResponse)
def status(user_id: str = "demo-user") -> LibraryStatusResponse:
    return library_status(user_id)
