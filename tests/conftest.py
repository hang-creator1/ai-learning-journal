"""Shared test fixtures.

Tests run without Qdrant or sentence-transformers:
- `embed_texts` is monkey-patched to a deterministic hash-based vector function.
- `get_store` returns an in-memory dict-based store with cosine search.

This keeps the suite fast (~sub-second) and offline.
"""

from __future__ import annotations

import hashlib
import math
import uuid
from dataclasses import dataclass, field
from typing import Any

import pytest
from fastapi.testclient import TestClient

from app.errors import CollectionNotFoundError
from app.main import app
from app.routes import v1 as v1_routes
from app.store import Hit

_DIM = 32  # small + fast for tests


def _hash_embed(text: str, dim: int = _DIM) -> list[float]:
    """Deterministic pseudo-embedding: SHA-256 → fixed-length float vector, L2 normalized."""
    h = hashlib.sha256(text.encode("utf-8")).digest()
    # Repeat hash bytes if dim > 32 (sha256 is 32 bytes); MiniLM is 384, here we use 32.
    raw = (h * ((dim // len(h)) + 1))[:dim]
    vec = [(b - 128) / 128.0 for b in raw]
    norm = math.sqrt(sum(x * x for x in vec)) or 1.0
    return [x / norm for x in vec]


def _stub_embed(texts: list[str]) -> list[list[float]]:
    return [_hash_embed(t) for t in texts]


@dataclass
class _Point:
    id: str
    vector: list[float]
    text: str
    metadata: dict[str, Any] = field(default_factory=dict)


class InMemoryStore:
    """Tiny dict-based replacement for `QdrantStore` used in tests."""

    def __init__(self) -> None:
        self._collections: dict[str, list[_Point]] = {}

    def ensure_collection(self, name: str) -> None:
        self._collections.setdefault(name, [])

    def upsert(
        self,
        collection: str,
        texts: list[str],
        vectors: list[list[float]],
        metadata: list[dict[str, Any]] | None = None,
    ) -> list[str]:
        self.ensure_collection(collection)
        meta = metadata or [{} for _ in texts]
        ids: list[str] = []
        for text, vec, m in zip(texts, vectors, meta):
            pid = str(uuid.uuid4())
            ids.append(pid)
            self._collections[collection].append(
                _Point(id=pid, vector=list(vec), text=text, metadata=dict(m))
            )
        return ids

    def search(self, collection: str, vector: list[float], top_k: int) -> list[Hit]:
        if collection not in self._collections:
            raise CollectionNotFoundError(f"Collection '{collection}' does not exist")
        scored: list[tuple[float, _Point]] = []
        for p in self._collections[collection]:
            scored.append((_cosine(vector, p.vector), p))
        scored.sort(key=lambda x: x[0], reverse=True)
        return [
            Hit(id=p.id, text=p.text, score=float(s), metadata=dict(p.metadata))
            for s, p in scored[:top_k]
        ]

    def delete_collection(self, name: str) -> None:
        if name not in self._collections:
            raise CollectionNotFoundError(f"Collection '{name}' does not exist")
        del self._collections[name]


def _cosine(a: list[float], b: list[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a)) or 1.0
    nb = math.sqrt(sum(x * x for x in b)) or 1.0
    return dot / (na * nb)


@pytest.fixture
def store() -> InMemoryStore:
    return InMemoryStore()


@pytest.fixture
def client(monkeypatch, store) -> TestClient:
    # Stub out the heavy embedding model.
    monkeypatch.setattr(v1_routes, "embed_texts", _stub_embed)
    # Replace Qdrant with the in-memory store via FastAPI dependency overrides.
    app.dependency_overrides[v1_routes.get_store] = lambda: store
    try:
        with TestClient(app) as c:
            yield c
    finally:
        app.dependency_overrides.pop(v1_routes.get_store, None)
