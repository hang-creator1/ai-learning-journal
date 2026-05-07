"""FastAPI application — public RAG API.

Versioned under /v1. Designed for B2B integration: stable contracts, OpenAPI
docs, clear error semantics, healthcheck for orchestrators.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app import __version__
from app.errors import RagError
from app.routes import v1

app = FastAPI(
    title="RAG Demo API",
    description="Retrieval-augmented generation over user-uploaded documents. "
    "FastAPI + Qdrant + sentence-transformers.",
    version=__version__,
    docs_url="/docs",
    openapi_url="/openapi.json",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET", "POST", "DELETE"],
    allow_headers=["*"],
)


@app.exception_handler(RagError)
async def rag_error_handler(_request, exc: RagError) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.code, "detail": exc.detail},
    )


@app.get("/health", tags=["meta"])
def health() -> dict[str, str]:
    """Liveness probe — orchestrators (Docker, K8s) hit this. No Qdrant call."""
    return {"status": "ok", "version": __version__}


@app.get("/", tags=["meta"])
def root() -> dict[str, str]:
    return {
        "name": "rag-fastapi-demo",
        "version": __version__,
        "docs": "/docs",
        "v1": "/v1",
    }


app.include_router(v1.router, prefix="/v1", tags=["v1"])
