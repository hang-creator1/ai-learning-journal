def test_health(client):
    r = client.get("/health")
    assert r.status_code == 200
    body = r.json()
    assert body["status"] == "ok"
    assert "version" in body


def test_root_lists_v1(client):
    r = client.get("/")
    assert r.status_code == 200
    assert r.json()["v1"] == "/v1"


def test_v1_index(client):
    r = client.get("/v1/")
    assert r.status_code == 200
    eps = r.json()["endpoints"]
    assert any("/v1/ingest" in e for e in eps)
    assert any("/v1/query" in e for e in eps)
    assert any("/v1/collection" in e for e in eps)


def test_openapi_published(client):
    r = client.get("/openapi.json")
    assert r.status_code == 200
    assert r.json()["info"]["title"] == "RAG Demo API"
