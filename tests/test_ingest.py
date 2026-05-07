def _doc() -> bytes:
    # Produces multiple chunks at chunk_size=200.
    body = (
        "FastAPI is a modern web framework. "
        "It is built on Starlette and Pydantic. "
        "Qdrant is a vector database written in Rust. "
        "Sentence-transformers wraps several embedding models. "
        "Retrieval-augmented generation grounds LLMs in your own data. "
    ) * 8
    return body.encode("utf-8")


def test_ingest_accepts_md(client):
    r = client.post(
        "/v1/ingest",
        files={"file": ("notes.md", _doc(), "text/markdown")},
        data={"collection": "demo", "chunk_size": "200", "chunk_overlap": "20"},
    )
    assert r.status_code == 200, r.text
    body = r.json()
    assert body["collection"] == "demo"
    assert body["chunks_added"] >= 2
    assert len(body["chunk_ids"]) == body["chunks_added"]


def test_ingest_accepts_txt(client):
    r = client.post(
        "/v1/ingest",
        files={"file": ("notes.txt", _doc(), "text/plain")},
        data={"collection": "demo"},
    )
    assert r.status_code == 200
    assert r.json()["chunks_added"] >= 1


def test_ingest_rejects_unsupported_extension(client):
    r = client.post(
        "/v1/ingest",
        files={"file": ("notes.pdf", b"hello", "application/pdf")},
    )
    assert r.status_code == 415
    assert r.json()["error"] == "invalid_file"


def test_ingest_rejects_empty_file(client):
    r = client.post(
        "/v1/ingest",
        files={"file": ("notes.txt", b"", "text/plain")},
    )
    assert r.status_code == 400
    assert r.json()["error"] == "empty_file"


def test_ingest_rejects_whitespace_only_file(client):
    r = client.post(
        "/v1/ingest",
        files={"file": ("notes.txt", b"   \n\n\t  ", "text/plain")},
    )
    assert r.status_code == 400
    assert r.json()["error"] == "empty_file"


def test_ingest_rejects_invalid_chunk_size(client):
    r = client.post(
        "/v1/ingest",
        files={"file": ("notes.txt", _doc(), "text/plain")},
        data={"chunk_size": "10"},
    )
    assert r.status_code == 422
    assert r.json()["error"] == "invalid_parameter"


def test_ingest_rejects_non_utf8(client):
    r = client.post(
        "/v1/ingest",
        files={"file": ("notes.txt", b"\xff\xfe\x00bad", "text/plain")},
    )
    assert r.status_code == 415
    assert r.json()["error"] == "invalid_file"
