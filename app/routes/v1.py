"""V1 of the RAG API.

Versioned under `/v1` so the contract can evolve (`/v2`) without breaking
existing integrations. Ingest is multipart (file upload + form fields), query
is JSON.
"""

from __future__ import annotations

import os
from typing import Annotated, Any

from fastapi import APIRouter, Depends, File, Form, UploadFile
from pydantic import BaseModel, Field

from app import embeddings as embeddings_mod
from app.chunking import chunk_text
from app.errors import EmptyFileError, InvalidFileError, InvalidParameterError
from app.store import QdrantStore

router = APIRouter()

_ALLOWED_SUFFIXES = (".md", ".txt")
_ALLOWED_MIMES = ("text/plain", "text/markdown", "application/octet-stream")


# ---------- DI ----------

_store_singleton: QdrantStore | None = None


def get_store() -> QdrantStore:
    """Default store provider — overridden in tests via `app.dependency_overrides`."""
    global _store_singleton
    if _store_singleton is None:
        _store_singleton = QdrantStore(dim=embeddings_mod.embedding_dim())
    return _store_singleton


def embed_texts(texts: list[str]) -> list[list[float]]:
    """Indirection so tests can monkey-patch this without touching the heavy model."""
    return embeddings_mod.embed(texts)


# ---------- Schemas ----------


class IngestResponse(BaseModel):
    collection: str
    chunks_added: int
    chunk_ids: list[str]


class QueryRequest(BaseModel):
    collection: str = "default"
    query: str = Field(min_length=1)
    top_k: int = Field(default=5, ge=1, le=50)
    synthesize: bool = False


class Chunk(BaseModel):
    id: str
    text: str
    score: float
    metadata: dict[str, Any]


class QueryResponse(BaseModel):
    chunks: list[Chunk]
    answer: str | None = None


# ---------- Endpoints ----------


@router.get("/")
def index() -> dict[str, list[str]]:
    """List of v1 operations."""
    return {
        "endpoints": [
            "POST /v1/ingest",
            "POST /v1/query",
            "DELETE /v1/collection/{name}",
        ],
    }


@router.post("/ingest", response_model=IngestResponse)
async def ingest(
    file: Annotated[UploadFile, File(description="Source document (.md or .txt)")],
    collection: Annotated[str, Form(description="Target Qdrant collection")] = "default",
    chunk_size: Annotated[int, Form(description="Chunk size in characters (100-2000)")] = 500,
    chunk_overlap: Annotated[int, Form(description="Overlap in characters (0-500)")] = 50,
    store: QdrantStore = Depends(get_store),
) -> IngestResponse:
    name = (file.filename or "").lower()
    if name and not name.endswith(_ALLOWED_SUFFIXES):
        raise InvalidFileError(f"Unsupported file type: only {', '.join(_ALLOWED_SUFFIXES)} allowed")

    raw = await file.read()
    if not raw:
        raise EmptyFileError("Empty file upload")

    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise InvalidFileError("File is not valid UTF-8 text") from exc

    if not text.strip():
        raise EmptyFileError("File contains no text content")

    if not collection:
        raise InvalidParameterError("`collection` cannot be empty")

    chunks = chunk_text(text, chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    if not chunks:
        raise EmptyFileError("File produced no chunks")

    vectors = embed_texts(chunks)
    metadata = [{"source": file.filename or "uploaded"} for _ in chunks]
    ids = store.upsert(collection, texts=chunks, vectors=vectors, metadata=metadata)
    return IngestResponse(collection=collection, chunks_added=len(ids), chunk_ids=ids)


@router.post("/query", response_model=QueryResponse)
def query(
    body: QueryRequest,
    store: QdrantStore = Depends(get_store),
) -> QueryResponse:
    vector = embed_texts([body.query])[0]
    hits = store.search(body.collection, vector=vector, top_k=body.top_k)
    chunks = [
        Chunk(id=h.id, text=h.text, score=h.score, metadata=h.metadata) for h in hits
    ]

    answer: str | None = None
    if body.synthesize and os.getenv("OPENAI_API_KEY"):
        answer = _synthesize(body.query, [c.text for c in chunks])

    return QueryResponse(chunks=chunks, answer=answer)


@router.delete("/collection/{name}")
def delete_collection(
    name: str,
    store: QdrantStore = Depends(get_store),
) -> dict[str, str]:
    store.delete_collection(name)
    return {"status": "deleted", "collection": name}


# ---------- Internal ----------


def _synthesize(query: str, contexts: list[str]) -> str | None:
    """Send retrieved chunks + query to OpenAI for an answer.

    Imported lazily so the API works without `openai` installed when synthesis
    is disabled.
    """
    try:
        from openai import OpenAI  # type: ignore
    except ImportError:
        return None

    if not contexts:
        return None

    prompt = (
        "Answer the question using ONLY the provided context. "
        "If the context is insufficient, say so plainly.\n\n"
        + "\n\n".join(f"[{i+1}] {c}" for i, c in enumerate(contexts))
        + f"\n\nQuestion: {query}\nAnswer:"
    )

    try:
        client = OpenAI()
        resp = client.chat.completions.create(
            model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
        )
        return (resp.choices[0].message.content or "").strip() or None
    except Exception:
        # Synthesis is best-effort; fall back to chunks-only.
        return None
