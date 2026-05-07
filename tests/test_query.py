def _ingest(client, *, collection: str = "demo", body: bytes | None = None) -> int:
    body = body or (
        b"FastAPI is a Python web framework.\n\n"
        b"Qdrant stores vectors with cosine distance.\n\n"
        b"Sentence-transformers produces dense embeddings.\n\n"
        b"Retrieval-augmented generation grounds LLMs in private data.\n\n"
    )
    r = client.post(
        "/v1/ingest",
        files={"file": ("notes.md", body, "text/markdown")},
        data={"collection": collection, "chunk_size": "120", "chunk_overlap": "10"},
    )
    assert r.status_code == 200, r.text
    return r.json()["chunks_added"]


def test_query_returns_chunks(client):
    n = _ingest(client)
    r = client.post(
        "/v1/query",
        json={"collection": "demo", "query": "what is FastAPI?", "top_k": 3},
    )
    assert r.status_code == 200, r.text
    body = r.json()
    assert body["answer"] is None  # synthesize=false by default
    assert 1 <= len(body["chunks"]) <= min(3, n)
    for ch in body["chunks"]:
        assert "id" in ch and "text" in ch and "score" in ch and "metadata" in ch


def test_query_respects_top_k(client):
    _ingest(client)
    r = client.post(
        "/v1/query",
        json={"collection": "demo", "query": "vectors", "top_k": 1},
    )
    assert r.status_code == 200
    assert len(r.json()["chunks"]) == 1


def test_query_missing_collection(client):
    r = client.post(
        "/v1/query",
        json={"collection": "nope", "query": "anything"},
    )
    assert r.status_code == 404
    assert r.json()["error"] == "collection_not_found"


def test_query_rejects_empty_query(client):
    r = client.post(
        "/v1/query",
        json={"collection": "demo", "query": ""},
    )
    assert r.status_code == 422


def test_query_synthesize_without_key_returns_null_answer(client, monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    _ingest(client)
    r = client.post(
        "/v1/query",
        json={"collection": "demo", "query": "vectors", "synthesize": True},
    )
    assert r.status_code == 200
    assert r.json()["answer"] is None


def test_delete_collection(client):
    _ingest(client, collection="todelete")
    r = client.delete("/v1/collection/todelete")
    assert r.status_code == 200
    assert r.json()["status"] == "deleted"

    # Subsequent query should now 404.
    r = client.post("/v1/query", json={"collection": "todelete", "query": "x"})
    assert r.status_code == 404


def test_delete_missing_collection(client):
    r = client.delete("/v1/collection/never-existed")
    assert r.status_code == 404
    assert r.json()["error"] == "collection_not_found"
