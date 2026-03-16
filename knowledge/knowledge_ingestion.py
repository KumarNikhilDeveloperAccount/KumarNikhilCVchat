from __future__ import annotations

import hashlib
import json
import re
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parent
DATA_ROOT = ROOT / "data"
RAW_ROOT = DATA_ROOT / "raw"
CHUNK_ROOT = DATA_ROOT / "chunks"
MANIFEST_PATH = DATA_ROOT / "manifest.json"


@dataclass
class SourceDefinition:
    key: str
    url: str
    license_name: str
    tags: list[str] = field(default_factory=list)
    format_hint: str = "html"


SOURCES = [
    SourceDefinition(
        key="wikipedia_en",
        url="https://dumps.wikimedia.org/enwiki/latest/",
        license_name="CC BY-SA 4.0",
        tags=["encyclopedia", "general", "wikipedia"],
        format_hint="xml",
    ),
    SourceDefinition(
        key="project_gutenberg_rdf",
        url="https://www.gutenberg.org/cache/epub/feeds/rdf-files.tar.bz2",
        license_name="Project Gutenberg license",
        tags=["books", "literature", "public-domain"],
        format_hint="tar.bz2",
    ),
    SourceDefinition(
        key="stackexchange_dump",
        url="https://archive.org/details/stackexchange",
        license_name="CC BY-SA 4.0",
        tags=["stackoverflow", "qna", "programming"],
        format_hint="7z",
    ),
    SourceDefinition(
        key="arxiv_bulk",
        url="https://info.arxiv.org/help/bulk_data.html",
        license_name="arXiv open access metadata and source terms",
        tags=["research", "arxiv", "papers"],
        format_hint="jsonl",
    ),
    SourceDefinition(
        key="pubmed_oa",
        url="https://ftp.ncbi.nlm.nih.gov/pub/pmc/",
        license_name="PubMed Central Open Access subset",
        tags=["research", "medical", "papers"],
        format_hint="xml",
    ),
    SourceDefinition(
        key="rfc_bulk",
        url="https://www.rfc-editor.org/retrieve/bulk/",
        license_name="IETF Trust Legal Provisions",
        tags=["rfc", "internet-standards"],
        format_hint="txt",
    ),
    SourceDefinition(
        key="w3c_specs",
        url="https://www.w3.org/TR/",
        license_name="W3C document license",
        tags=["w3c", "web-standards"],
        format_hint="html",
    ),
    SourceDefinition(
        key="aws_docs",
        url="https://docs.aws.amazon.com/",
        license_name="AWS site terms",
        tags=["cloud", "aws", "docs"],
        format_hint="html",
    ),
    SourceDefinition(
        key="azure_docs",
        url="https://learn.microsoft.com/azure/",
        license_name="Microsoft Learn terms",
        tags=["cloud", "azure", "docs"],
        format_hint="html",
    ),
    SourceDefinition(
        key="gcp_docs",
        url="https://cloud.google.com/docs",
        license_name="Google Cloud documentation terms",
        tags=["cloud", "gcp", "docs"],
        format_hint="html",
    ),
    SourceDefinition(
        key="kubernetes_docs",
        url="https://kubernetes.io/docs/home/",
        license_name="CC BY 4.0",
        tags=["cloud", "kubernetes", "docs"],
        format_hint="html",
    ),
]


@dataclass
class ChunkRecord:
    chunk_id: str
    source_key: str
    title: str
    content: str
    tags: list[str]
    metadata: dict[str, str]
    updated_at: str


def ensure_dirs() -> None:
    for directory in [DATA_ROOT, RAW_ROOT, CHUNK_ROOT]:
        directory.mkdir(parents=True, exist_ok=True)


def normalize_text(text: str) -> str:
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def semantic_hierarchical_chunk(text: str, source_key: str, title: str, tags: list[str]) -> list[ChunkRecord]:
    paragraphs = [normalize_text(part) for part in re.split(r"\n{2,}|(?<=\.)\s{2,}", text) if normalize_text(part)]
    chunks: list[ChunkRecord] = []
    buffer: list[str] = []
    for paragraph in paragraphs:
        buffer.append(paragraph)
        candidate = " ".join(buffer)
        if len(candidate) < 950:
            continue
        chunks.append(build_chunk(source_key, title, candidate, tags))
        overlap = candidate[-180:]
        buffer = [overlap]
    if buffer:
        chunks.append(build_chunk(source_key, title, " ".join(buffer), tags))
    return chunks


def build_chunk(source_key: str, title: str, content: str, tags: list[str]) -> ChunkRecord:
    normalized = normalize_text(content)
    chunk_id = hashlib.sha256(f"{source_key}:{title}:{normalized}".encode("utf-8")).hexdigest()
    return ChunkRecord(
        chunk_id=chunk_id,
        source_key=source_key,
        title=title,
        content=normalized,
        tags=tags,
        metadata={
            "difficulty": infer_difficulty(normalized),
            "source_type": source_key,
        },
        updated_at=datetime.now(tz=UTC).isoformat(),
    )


def infer_difficulty(text: str) -> str:
    lowered = text.lower()
    advanced_markers = ["kubernetes", "distributed", "compiler", "consensus", "zero trust", "raft"]
    if any(marker in lowered for marker in advanced_markers):
        return "advanced"
    if len(text.split()) > 180:
        return "intermediate"
    return "beginner"


def deduplicate_chunks(chunks: Iterable[ChunkRecord]) -> list[ChunkRecord]:
    unique: dict[str, ChunkRecord] = {}
    for chunk in chunks:
        unique[chunk.chunk_id] = chunk
    return list(unique.values())


def write_manifest() -> None:
    ensure_dirs()
    MANIFEST_PATH.write_text(
        json.dumps(
            {
                "generated_at": datetime.now(tz=UTC).isoformat(),
                "sources": [asdict(source) for source in SOURCES],
            },
            indent=2,
        ),
        encoding="utf-8",
    )


def ingest_local_document(source_key: str, title: str, text: str, tags: list[str]) -> list[ChunkRecord]:
    ensure_dirs()
    chunks = deduplicate_chunks(semantic_hierarchical_chunk(text, source_key, title, tags))
    output_path = CHUNK_ROOT / f"{source_key}-{slugify(title)}.json"
    output_path.write_text(json.dumps([asdict(chunk) for chunk in chunks], indent=2), encoding="utf-8")
    return chunks


def slugify(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")


if __name__ == "__main__":
    write_manifest()
    demo_text = (
        "Kubernetes automates deployment, scaling, and recovery for containerized workloads. "
        "It groups containers into pods and uses declarative APIs for state management.\n\n"
        "Production clusters require observability, RBAC, network policy, capacity planning, "
        "and resilient rollout strategy."
    )
    created = ingest_local_document("demo", "Kubernetes Primer", demo_text, ["cloud", "kubernetes"])
    print(f"wrote {len(created)} chunk records to {CHUNK_ROOT}")
