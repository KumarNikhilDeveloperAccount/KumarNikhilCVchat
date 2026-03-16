from __future__ import annotations

import json
import re
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any
from uuid import uuid4

from ..models import (
    KnowledgeIngestRequest,
    KnowledgeIngestResponse,
    KnowledgeItem,
    LibraryStatusResponse,
)


@dataclass
class MemoryChunk:
    source: str
    trust: float
    text: str


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
CV_PROFILE_PATH = DATA_DIR / "kumar_nikhil_cv.json"

STOPWORDS = {
    "a",
    "an",
    "and",
    "are",
    "about",
    "define",
    "explain",
    "for",
    "how",
    "i",
    "is",
    "me",
    "of",
    "tell",
    "the",
    "to",
    "was",
    "what",
    "who",
}


def tokenize(text: str) -> set[str]:
    return {
        token
        for token in re.findall(r"[a-z0-9\-\+\.#]+", text.lower())
        if len(token) > 1 and token not in STOPWORDS
    }


def load_json(path: Path) -> Any:
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def build_cv_library() -> list[dict[str, Any]]:
    profile = load_json(CV_PROFILE_PATH) or {}
    if not profile:
        return []

    items: list[dict[str, Any]] = [
        {
            "id": str(uuid4()),
            "title": "Kumar Nikhil Profile Summary",
            "content": profile["summary"],
            "tags": ["kumar-nikhil", "summary", "cv", "profile"],
            "source_kind": "cv",
            "trust": 0.99,
        },
        {
            "id": str(uuid4()),
            "title": "Kumar Nikhil Contact",
            "content": f"{profile['identity']['name']} is based in {profile['identity']['location']}. Contact details: phone {profile['identity']['phone']}, email {profile['identity']['email']}.",
            "tags": ["kumar-nikhil", "contact", "identity", "cv"],
            "source_kind": "cv",
            "trust": 0.99,
        },
        {
            "id": str(uuid4()),
            "title": "Kumar Nikhil Certifications",
            "content": "Certifications: " + "; ".join(profile.get("certifications", [])) + ".",
            "tags": ["kumar-nikhil", "certifications", "cv"],
            "source_kind": "cv",
            "trust": 0.99,
        },
        {
            "id": str(uuid4()),
            "title": "Kumar Nikhil Education",
            "content": "Education timeline: " + "; ".join(profile.get("education", [])) + ".",
            "tags": ["kumar-nikhil", "education", "cv"],
            "source_kind": "cv",
            "trust": 0.99,
        },
        {
            "id": str(uuid4()),
            "title": "Kumar Nikhil Skills",
            "content": "Core skills and technologies: " + "; ".join(profile.get("skills", [])) + ".",
            "tags": ["kumar-nikhil", "skills", "technology", "cv"],
            "source_kind": "cv",
            "trust": 0.99,
        },
        {
            "id": str(uuid4()),
            "title": "Kumar Nikhil Languages",
            "content": "Languages: " + "; ".join(profile.get("languages", [])) + ".",
            "tags": ["kumar-nikhil", "languages", "cv"],
            "source_kind": "cv",
            "trust": 0.99,
        },
        {
            "id": str(uuid4()),
            "title": "Kumar Nikhil Internships and Activities",
            "content": "Trainings and internships: " + "; ".join(profile.get("internships", [])) + ".",
            "tags": ["kumar-nikhil", "internships", "activities", "cv"],
            "source_kind": "cv",
            "trust": 0.98,
        },
    ]

    for role in profile.get("experience", []):
        items.append(
            {
                "id": str(uuid4()),
                "title": f"{role['company']} - {role['role']}",
                "content": f"{role['role']} at {role['company']} ({role['duration']}). Highlights: " + "; ".join(role.get("highlights", [])) + ".",
                "tags": ["kumar-nikhil", "experience", "career", "cv", "dxc"],
                "source_kind": "cv",
                "trust": 0.99,
            }
        )
    return items


CV_LIBRARY = build_cv_library()

MEMORY_STORE: dict[str, list[dict[str, Any]]] = {
    "demo-user": [
        {
            "source": "profile_mode",
            "trust": 0.99,
            "text": "This experience is Kumar Nikhil's personalized AI chat CV and should focus on his profile, background, skills, certifications, and work history.",
        }
    ]
}

KNOWLEDGE_STORE: dict[str, list[dict[str, Any]]] = {"demo-user": []}


def score_entry(item: dict[str, Any], query_tokens: set[str], raw_query: str) -> tuple[int, float]:
    haystack_text = " ".join(
        [
            item.get("title", ""),
            item.get("content", ""),
            " ".join(item.get("tags", [])),
        ]
    )
    haystack_tokens = tokenize(haystack_text)
    title_tokens = tokenize(item.get("title", ""))
    score = 0
    for token in query_tokens:
        if token in haystack_tokens:
            score += 3 if token in title_tokens else 1

    lowered_query = raw_query.lower().strip().rstrip("?")
    title = item.get("title", "").lower()
    if lowered_query.endswith(title) or title in lowered_query:
        score += 6
    if "kumar" in lowered_query or "nikhil" in lowered_query:
        if "kumar-nikhil" in item.get("tags", []):
            score += 6

    return score, float(item.get("trust", 0.0))


def normalize_profile_query(message: str) -> str:
    lowered = message.lower()
    if any(token in lowered for token in [" he ", " his ", " him ", " he?", " his?", " him?", "where does he", "does he"]):
        return f"Kumar Nikhil {message}"
    return message


def retrieve_memories(user_id: str, message: str) -> list[MemoryChunk]:
    entries = MEMORY_STORE.get(user_id, [])
    query_tokens = tokenize(message)
    ranked = sorted(
        entries,
        key=lambda item: (
            sum(1 for token in query_tokens if token in item["text"].lower()),
            item["trust"],
        ),
        reverse=True,
    )
    filtered = [
        MemoryChunk(**item)
        for item in ranked
        if sum(1 for token in query_tokens if token in item["text"].lower()) > 0
        or item["source"] == "profile_mode"
    ]
    return filtered[:3]


def retrieve_knowledge(user_id: str, message: str) -> list[KnowledgeItem]:
    normalized_message = normalize_profile_query(message)
    query_tokens = tokenize(normalized_message)
    if not query_tokens:
        return []

    user_entries = KNOWLEDGE_STORE.get(user_id, [])
    combined = list(user_entries) + list(CV_LIBRARY)
    ranked = sorted(
        combined,
        key=lambda item: score_entry(item, query_tokens, normalized_message),
        reverse=True,
    )
    seen: set[str] = set()
    filtered: list[KnowledgeItem] = []
    for item in ranked:
        score, _ = score_entry(item, query_tokens, normalized_message)
        if score <= 0:
            continue
        key = f"{item.get('title')}::{item.get('content')[:80]}"
        if key in seen:
            continue
        seen.add(key)
        filtered.append(KnowledgeItem(**item))
        if len(filtered) >= 6:
            break
    return filtered


def extract_memory(user_id: str, message: str) -> None:
    lowered = message.lower()
    if "prefer" in lowered or "focus" in lowered:
        MEMORY_STORE.setdefault(user_id, []).append(
            {
                "source": "chat_inference",
                "trust": 0.74,
                "text": f"Recent stated preference: {message.strip()}",
            }
        )


def ingest_knowledge(payload: KnowledgeIngestRequest) -> KnowledgeIngestResponse:
    item = KnowledgeItem(
        id=str(uuid4()),
        title=payload.title.strip(),
        content=payload.content.strip(),
        tags=payload.tags,
        source_kind=payload.source_kind,
        trust=0.88,
    )
    KNOWLEDGE_STORE.setdefault(payload.user_id, []).append(item.model_dump())
    return KnowledgeIngestResponse(saved=True, item=item)


def list_knowledge(user_id: str) -> list[KnowledgeItem]:
    return [KnowledgeItem(**item) for item in KNOWLEDGE_STORE.get(user_id, [])]


def library_status(user_id: str) -> LibraryStatusResponse:
    user_documents = len(KNOWLEDGE_STORE.get(user_id, []))
    cv_documents = len(CV_LIBRARY)
    last_updated = datetime.fromtimestamp(
        CV_PROFILE_PATH.stat().st_mtime if CV_PROFILE_PATH.exists() else datetime.now(tz=UTC).timestamp(),
        tz=UTC,
    ).isoformat()
    return LibraryStatusResponse(
        total_documents=user_documents + cv_documents,
        user_documents=user_documents + cv_documents,
        global_documents=0,
        last_updated=last_updated,
        headline="Personalized AI CV mode is active. This assistant is optimized around Kumar Nikhil's profile, experience, skills, and credentials.",
    )
