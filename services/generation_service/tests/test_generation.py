from unittest.mock import MagicMock, patch

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200


def test_generate_returns_stub_when_unconfigured():
    with patch("app.main.settings") as mock_settings:
        mock_settings.gemini_api_key = ""
        mock_settings.gemini_model = "gemini-3.6-flash"
        response = client.post("/generate", json={"prompt": "Write a haiku"})
    assert response.status_code == 200
    body = response.json()
    assert "Write a haiku" in body["output"]
    assert body["output"].startswith("[stub output")


def test_refine_returns_stub_when_unconfigured():
    with patch("app.main.settings") as mock_settings:
        mock_settings.gemini_api_key = ""
        mock_settings.gemini_model = "gemini-3.6-flash"
        response = client.post(
            "/refine", json={"content": "hello world", "instructions": "make it shorter"}
        )
    assert response.status_code == 200
    body = response.json()
    assert "make it shorter" in body["output"]
    assert "hello world" in body["output"]


def _fake_gemini_response(text: str) -> MagicMock:
    fake = MagicMock()
    fake.raise_for_status.return_value = None
    fake.json.return_value = {"candidates": [{"content": {"parts": [{"text": text}]}}]}
    return fake


def test_generate_calls_gemini_with_correct_request_when_configured():
    with patch("app.main.settings") as mock_settings, patch("httpx.post") as mock_post:
        mock_settings.gemini_api_key = "gm-test"
        mock_settings.gemini_base_url = "https://generativelanguage.googleapis.com/v1beta/models"
        mock_settings.gemini_model = "gemini-3.6-flash"
        mock_post.return_value = _fake_gemini_response("A generated haiku")

        response = client.post("/generate", json={"prompt": "Write a haiku"})

        assert response.status_code == 200
        assert response.json()["output"] == "A generated haiku"

        call = mock_post.call_args
        assert call.args[0] == "https://generativelanguage.googleapis.com/v1beta/models/gemini-3.6-flash:generateContent"
        assert call.kwargs["params"] == {"key": "gm-test"}
        assert call.kwargs["json"] == {"contents": [{"parts": [{"text": "Write a haiku"}]}]}


def test_generate_returns_502_when_gemini_unreachable():
    with patch("app.main.settings") as mock_settings, patch("httpx.post") as mock_post:
        mock_settings.gemini_api_key = "gm-test"
        mock_settings.gemini_base_url = "https://generativelanguage.googleapis.com/v1beta/models"
        mock_settings.gemini_model = "gemini-3.6-flash"
        import httpx

        mock_post.side_effect = httpx.ConnectError("connection refused")

        response = client.post("/generate", json={"prompt": "hi"})
        assert response.status_code == 502
