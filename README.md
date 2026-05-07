# rag-fastapi-demo

Public REST API demo for **retrieval-augmented generation**: upload a document,
chunk it, embed each chunk with a local sentence-transformer, store vectors in
**Qdrant**, then query with semantic search and (optionally) synthesize an
answer with an LLM.

Built on **FastAPI + Qdrant + sentence-transformers**, packaged with `uv`,
dockerised, tested with `pytest`. Designed as a small but realistic example of
how to ship a RAG service: versioning, typed contracts, OpenAPI docs,
healthchecks, and clear error semantics.

## Endpoints

| Method | Path                      | Description                                               |
|--------|---------------------------|-----------------------------------------------------------|
| GET    | `/health`                 | Liveness probe (orchestrators, K8s, Docker) — no DB call  |
| GET    | `/`                       | Service metadata + entry points                           |
| GET    | `/v1/`                    | List of v1 operations                                     |
| POST   | `/v1/ingest`              | Upload `.md` / `.txt`, chunk, embed, upsert into Qdrant   |
| POST   | `/v1/query`               | Semantic search (top-k) with optional LLM synthesis       |
| DELETE | `/v1/collection/{name}`   | Drop a Qdrant collection                                  |
| GET    | `/docs`                   | Swagger UI                                                |
| GET    | `/openapi.json`           | OpenAPI 3 schema                                          |

`/v1/ingest` accepts `multipart/form-data`. `/v1/query` accepts JSON.

## Quick start

```bash
# Local dev (requires uv) — needs Qdrant running, e.g. `docker compose up qdrant`
uv sync --extra dev
uv run uvicorn app.main:app --reload

# Tests (no Qdrant or model download needed — fully mocked)
uv run pytest

# Full stack (API + Qdrant)
docker compose up --build
curl -fsS http://localhost:8000/health
```

The first ingest/query call downloads the embedding model
(`sentence-transformers/all-MiniLM-L6-v2`, ~90MB) into the cache. Subsequent
calls are warm and run in milliseconds.

## Examples

```bash
# Ingest a markdown file into the "demo" collection
curl -X POST http://localhost:8000/v1/ingest \
    -F "file=@notes.md" \
    -F "collection=demo" \
    -F "chunk_size=500" \
    -F "chunk_overlap=50"
# → {"collection":"demo","chunks_added":12,"chunk_ids":["..."]}

# Query — chunks only
curl -X POST http://localhost:8000/v1/query \
    -H "Content-Type: application/json" \
    -d '{"collection":"demo","query":"how does chunking work?","top_k":3}'

# Query — with LLM synthesis (requires OPENAI_API_KEY)
curl -X POST http://localhost:8000/v1/query \
    -H "Content-Type: application/json" \
    -d '{"collection":"demo","query":"summarise the doc","top_k":5,"synthesize":true}'

# Drop a collection
curl -X DELETE http://localhost:8000/v1/collection/demo
```

## Design notes

**Versioning.** The public surface lives under `/v1` so future breaking
changes (e.g., chunking defaults, response shape) ship as `/v2` without
forcing existing clients to migrate. Meta endpoints (`/health`, `/`, `/docs`)
sit outside the version prefix because they describe the service, not the
contract.

**Chunking strategy — sentence-aware overlap.** `app/chunking.py` is a pure
function over `str`. It targets `chunk_size` characters but prefers to break
on the largest available semantic boundary (`\n\n`, `\n`, `. `, `! `, `? `,
` `) within a window before the target. Overlap is character-based and
applied between adjacent chunks so retrieval doesn't lose context across
boundaries. Pure-function design means the layer is trivial to unit-test
today and easy to swap (e.g., for `tiktoken`-based token chunking) tomorrow.

**Why MiniLM?** `sentence-transformers/all-MiniLM-L6-v2` is the default
because it's small (~90MB), fast (CPU-friendly), and crucially **needs no
API key** — the demo runs end-to-end offline. The embedding layer is a thin
wrapper (`app/embeddings.py`) so swapping to `bge-large`, `nomic-embed`, or
a hosted embedding API is a one-line change.

**Qdrant as the vector store.** Cosine distance, auto-created collections
sized to the embedding dimension. Chosen over pgvector for this demo because
it ships as a single container with zero schema work, and over Pinecone
because it runs locally without an account. The `app/store.py` wrapper
exposes a minimal interface (`upsert`, `search`, `delete_collection`) so the
backend is replaceable.

**Hybrid search — future work.** Pure dense retrieval is good enough for
this demo, but production RAG benefits from BM25 + dense fusion (e.g.,
RRF). Qdrant supports sparse vectors natively; the wrapper would grow a
`search_hybrid` method without changing the route surface.

**Stable error codes.** Errors return `{ "error": "<code>", "detail":
"<message>" }` with a stable string code (`invalid_file`, `empty_file`,
`invalid_parameter`, `collection_not_found`). Clients can switch on `error`
without parsing prose.

**Healthcheck contract.** `GET /health` is the contract orchestrators rely
on (Docker, ECS, K8s). It is intentionally lightweight: **no Qdrant call,
no model load** — returns `{status, version}`. Liveness ≠ readiness; if the
upstream vector DB is down, ingest/query will surface that on their own
paths rather than flapping the container.

**Optional LLM synthesis.** When `OPENAI_API_KEY` is set and a request
passes `synthesize=true`, retrieved chunks are stuffed into a constrained
prompt ("answer using only the context") and sent to a small chat model.
Without the key, the endpoint silently returns `answer: null` and the
chunks — keeping the API useful as a pure retrieval service.

## Project layout

```
rag-fastapi-demo/
├── app/
│   ├── __init__.py
│   ├── main.py            # FastAPI app, CORS, error handler, /health, /
│   ├── errors.py          # RagError + typed subclasses
│   ├── chunking.py        # Pure-function chunker (sentence-aware overlap)
│   ├── embeddings.py      # sentence-transformers wrapper (lazy singleton)
│   ├── store.py           # Qdrant client wrapper
│   └── routes/
│       └── v1.py          # /v1/ingest, /v1/query, /v1/collection/{name}
├── tests/
│   ├── conftest.py        # TestClient + in-memory store + stub embedder
│   ├── test_meta.py
│   ├── test_chunking.py
│   ├── test_ingest.py
│   └── test_query.py
├── Dockerfile
├── docker-compose.yml     # api + qdrant
├── pyproject.toml
└── README.md
```

## Tech

- **Python** 3.11+
- **FastAPI** 0.115+
- **Pydantic** v2
- **Qdrant** + `qdrant-client` 1.12+
- **sentence-transformers** 3+ (default model: `all-MiniLM-L6-v2`, 384-dim, cosine)
- **OpenAI** SDK (optional, for synthesis only)
- **uvicorn** with the `[standard]` extras (httptools, uvloop, websockets)
- **pytest** + FastAPI's `TestClient` (Qdrant + embedder fully mocked)
- **uv** for dependency management

## License

MIT — see header in `pyproject.toml`.

---
