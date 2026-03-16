from __future__ import annotations

import math
import re
from collections import Counter
from dataclasses import dataclass


@dataclass
class RetrievedChunk:
    chunk_id: str
    title: str
    content: str
    score: float
    source_key: str


class HybridRAGEngine:
    def __init__(self, vector_store, graph_store=None, bm25_index=None):
        self.vector_store = vector_store
        self.graph_store = graph_store
        self.bm25_index = bm25_index

    def answer_plan(self, query: str, user_memory: list[dict] | None = None) -> dict:
        rewritten_queries = self.expand_queries(query)
        vector_hits = self.vector_search(rewritten_queries)
        lexical_hits = self.lexical_search(rewritten_queries)
        graph_hits = self.graph_search(query)
        merged = self.rerank(vector_hits + lexical_hits + graph_hits)
        return {
            "query": query,
            "rewritten_queries": rewritten_queries,
            "top_chunks": [chunk.__dict__ for chunk in merged[:8]],
            "user_memory": user_memory or [],
            "compression_hint": self.compression_hint(merged[:8]),
        }

    def expand_queries(self, query: str) -> list[str]:
        lowered = query.lower()
        expansions = [query]
        if "kubernetes" in lowered:
            expansions.extend(["k8s cluster design", "kubernetes best practices", "kubernetes troubleshooting"])
        if "aws" in lowered:
            expansions.extend(["aws architecture", "aws best practices", "aws security design"])
        if "debug" in lowered:
            expansions.append("root cause analysis steps")
        return list(dict.fromkeys(expansions))

    def vector_search(self, queries: list[str]) -> list[RetrievedChunk]:
        if self.vector_store is None:
            return []
        hits: list[RetrievedChunk] = []
        for query in queries:
            for item in self.vector_store.search(query, limit=6):
                hits.append(RetrievedChunk(**item))
        return hits

    def lexical_search(self, queries: list[str]) -> list[RetrievedChunk]:
        if self.bm25_index is None:
            return []
        hits: list[RetrievedChunk] = []
        for query in queries:
            for item in self.bm25_index.search(query, limit=6):
                hits.append(RetrievedChunk(**item))
        return hits

    def graph_search(self, query: str) -> list[RetrievedChunk]:
        if self.graph_store is None:
            return []
        entities = re.findall(r"[A-Z][A-Za-z0-9\-\+\.]+", query)
        hits: list[RetrievedChunk] = []
        for entity in entities:
            for item in self.graph_store.lookup(entity):
                hits.append(RetrievedChunk(**item))
        return hits

    def rerank(self, chunks: list[RetrievedChunk]) -> list[RetrievedChunk]:
        merged: dict[str, RetrievedChunk] = {}
        for chunk in chunks:
            if chunk.chunk_id not in merged or merged[chunk.chunk_id].score < chunk.score:
                merged[chunk.chunk_id] = chunk
        return sorted(merged.values(), key=lambda item: item.score, reverse=True)

    def compression_hint(self, chunks: list[RetrievedChunk]) -> dict:
        token_budget = 12000
        average_chars = sum(len(chunk.content) for chunk in chunks) / max(len(chunks), 1)
        return {
            "target_token_budget": token_budget,
            "compression_ratio": round(min(1.0, token_budget / max(average_chars, 1)) / 4, 3),
            "strategy": "summarize low-score chunks, keep citations, preserve user memory separately",
        }


class SimpleBM25Index:
    def __init__(self, documents: list[dict]):
        self.documents = documents
        self.doc_freq = Counter()
        self.avg_len = 0.0
        for doc in documents:
            tokens = self._tokenize(doc["content"])
            self.avg_len += len(tokens)
            for token in set(tokens):
                self.doc_freq[token] += 1
        self.avg_len = self.avg_len / max(len(documents), 1)

    def search(self, query: str, limit: int = 6) -> list[dict]:
        q_tokens = self._tokenize(query)
        results: list[dict] = []
        doc_count = len(self.documents)
        for doc in self.documents:
            tokens = self._tokenize(doc["content"])
            if not tokens:
                continue
            counts = Counter(tokens)
            score = 0.0
            for token in q_tokens:
                if token not in counts:
                    continue
                idf = math.log(((doc_count - self.doc_freq[token]) + 0.5) / (self.doc_freq[token] + 0.5) + 1)
                tf = counts[token]
                score += idf * ((tf * 2.2) / (tf + 1.2 * (1 - 0.75 + 0.75 * len(tokens) / max(self.avg_len, 1))))
            if score > 0:
                results.append(
                    {
                        "chunk_id": doc["chunk_id"],
                        "title": doc["title"],
                        "content": doc["content"],
                        "score": round(score, 4),
                        "source_key": doc["source_key"],
                    }
                )
        return sorted(results, key=lambda item: item["score"], reverse=True)[:limit]

    @staticmethod
    def _tokenize(text: str) -> list[str]:
        return re.findall(r"[a-z0-9\-\+\.#]+", text.lower())
