from __future__ import annotations

from ..models import ChatRequest, ChatResponse, Usage
from .memory import extract_memory, retrieve_knowledge, retrieve_memories
from .prompting import build_prompt
from .providers import generate_response, select_model


def handle_chat(payload: ChatRequest) -> ChatResponse:
    memories = retrieve_memories(payload.user_id, payload.message)
    knowledge = retrieve_knowledge(payload.user_id, payload.message)
    prompt = build_prompt(payload.message, memories, knowledge)
    model_used = select_model(payload.message)
    response_text = generate_response(model_used, prompt)
    extract_memory(payload.user_id, payload.message)

    theme_hint = "royal"

    usage = Usage(
        prompt_tokens=max(32, len(payload.message.split()) * 8),
        completion_tokens=max(48, len(response_text.split()) * 2),
    )

    return ChatResponse(
        model_used=model_used,
        response=response_text,
        memory_used=bool(memories),
        theme_hint=theme_hint,
        usage=usage,
        retrieved_memories=[memory.__dict__ for memory in memories],
        retrieved_knowledge=[item.model_dump() for item in knowledge],
    )
