from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200


def test_generate_returns_stub_when_unconfigured():
    response = client.post("/generate", json={"prompt": "Write a haiku"})
    assert response.status_code == 200
    body = response.json()
    assert "Write a haiku" in body["output"]
    assert body["output"].startswith("[stub output")


def test_refine_returns_stub_when_unconfigured():
    response = client.post(
        "/refine", json={"content": "hello world", "instructions": "make it shorter"}
    )
    assert response.status_code == 200
    body = response.json()
    assert "make it shorter" in body["output"]
    assert "hello world" in body["output"]
