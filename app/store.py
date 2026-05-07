"""Vector store — Qdrant client wrapper.

Thin façade over `qdrant-client`. Pure-data inputs/outputs so tests can swap
the implementation with an in-memory dict-based store (see `tests/conftest.py`).
"""

from __future__ import annotations

import os
import uuid
from dataclasses import dataclass
from typing import Any

from qdrant_client import QdrantClient
from qdrant_client.http import models as rest

from app.errors import CollectionNotFoundError


@dataclass
class Hit:
    id: str
    text: str
    score: float
    metadata: dict[str, Any]


class QdrantStore:
    """Wrapper around `qdrant-client` exposing the minimal RAG ops we need."""

    def __init__(self, url: str | None = None, dim: int = 384) -> None:
        self._url = url or os.getenv("QDRANT_URL", "http://localhost:6333")
        self._dim = dim
        self._client = QdrantClient(url=self._url)

    def ensure_collection(self, name: str) -> None:
        existing = {c.name for c in self._client.get_collections().collections}
        if name in existing:
            return
        self._client.create_collection(
            collection_name=name,
            vectors_config=rest.VectorParams(size=self._dim, distance=rest.Distance.COSINE),
        )

    def upsert(
        self,
        collection: str,
        texts: list[str],
        vectors: list[list[float]],
        metadata: list[dict[str, Any]] | None = None,
    ) -> list[str]:
        if not texts:
            return []
        self.ensure_collection(collection)

        ids = [str(uuid.uuid4()) for _ in texts]
        meta = metadata or [{} for _ in texts]
        points = [
            rest.PointStruct(
                id=pid,
                vector=vec,
                payload={"text": text, **m},
            )
            for pid, text, vec, m in zip(ids, texts, vectors, meta)
        ]
        self._client.upsert(collection_name=collection, points=points)
        return ids

    def search(self, collection: str, vector: list[float], top_k: int) -> list[Hit]:
        try:
            results = self._client.search(
                collection_name=collection,
                query_vector=vector,
                limit=top_k,
            )
        except Exception as exc:  # qdrant raises a generic error on missing collection
            msg = str(exc).lower()
            if "not found" in msg or "doesn't exist" in msg or "404" in msg:
                raise CollectionNotFoundError(f"Collection '{collection}' does not exist") from exc
            raise

        hits: list[Hit] = []
        for r in results:
            payload = dict(r.payload or {})
            text = str(payload.pop("text", ""))
            hits.append(Hit(id=str(r.id), text=text, score=float(r.score), metadata=payload))
        return hits

    def delete_collection(self, name: str) -> None:
        existing = {c.name for c in self._client.get_collections().collections}
        if name not in existing:
            raise CollectionNotFoundError(f"Collection '{name}' does not exist")
        self._client.delete_collection(collection_name=name)
