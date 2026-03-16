from typing import Any
from uuid import uuid4

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    conversation_id: str | None = None
    message: str
    platform: str = "web"
    theme_context: str = "elegant"
    mode: str = "standard"
    user_id: str = "demo-user"


class KnowledgeIngestRequest(BaseModel):
    user_id: str = "demo-user"
    title: str
    content: str
    tags: list[str] = Field(default_factory=list)
    source_kind: str = "manual"


class KnowledgeItem(BaseModel):
    id: str
    title: str
    content: str
    tags: list[str]
    source_kind: str
    trust: float


class Usage(BaseModel):
    prompt_tokens: int
    completion_tokens: int


class ChatResponse(BaseModel):
    message_id: str = Field(default_factory=lambda: str(uuid4()))
    model_used: str
    response: str
    memory_used: bool
    theme_hint: str
    usage: Usage
    retrieved_memories: list[dict[str, Any]]
    retrieved_knowledge: list[dict[str, Any]]


class ThemeGenerateRequest(BaseModel):
    base_theme: str
    intent: str


class ThemeGenerateResponse(BaseModel):
    theme_id: str
    tokens: dict[str, Any]


class KnowledgeIngestResponse(BaseModel):
    saved: bool
    item: KnowledgeItem


class KnowledgeListResponse(BaseModel):
    items: list[KnowledgeItem]


class LibraryStatusResponse(BaseModel):
    total_documents: int
    user_documents: int
    global_documents: int
    last_updated: str
    headline: str
