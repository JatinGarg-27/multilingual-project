from unittest.mock import MagicMock, patch

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health():
    assert client.get("/health").status_code == 200


def test_list_languages_covers_all_six():
    response = client.get("/languages")
    assert response.status_code == 200
    assert set(response.json()) == {"de", "fr", "es", "ta", "te", "kn"}


def test_default_voice_for_supported_language():
    response = client.get("/voices/ta")
    assert response.status_code == 200
    assert response.json()["language"] == "ta"
    assert response.json()["voice_id"]


def test_default_voice_rejects_unsupported_language():
    response = client.get("/voices/xx")
    assert response.status_code == 400


def test_synthesize_returns_stub_audio_when_unconfigured():
    response = client.post(
        "/synthesize", json={"text": "hola", "language": "es", "voice_id": "default-es"}
    )
    assert response.status_code == 200
    assert response.json()["audio_url"].startswith("stub://")


def test_synthesize_rejects_unsupported_language():
    response = client.post(
        "/synthesize", json={"text": "hi", "language": "xx", "voice_id": "v1"}
    )
    assert response.status_code == 400


def _fake_elevenlabs_response(audio_bytes: bytes) -> MagicMock:
    fake = MagicMock()
    fake.raise_for_status.return_value = None
    fake.content = audio_bytes
    return fake


def test_synthesize_calls_elevenlabs_and_serves_the_file_when_configured():
    with patch("app.main.settings") as mock_settings, patch("httpx.post") as mock_post:
        mock_settings.elevenlabs_api_key = "el-test"
        mock_settings.elevenlabs_base_url = "https://api.elevenlabs.io/v1/text-to-speech"
        mock_settings.elevenlabs_model_id = "eleven_multilingual_v2"
        mock_settings.public_base_url = "http://localhost:8002"
        mock_settings.supported_languages = ("de", "fr", "es", "ta", "te", "kn")
        mock_post.return_value = _fake_elevenlabs_response(b"fake-mp3-bytes")

        response = client.post(
            "/synthesize", json={"text": "Bonjour", "language": "fr", "voice_id": "abc123"}
        )

        assert response.status_code == 200
        audio_url = response.json()["audio_url"]
        assert audio_url.startswith("http://localhost:8002/audio/")
        assert audio_url.endswith(".mp3")

        call = mock_post.call_args
        assert call.args[0] == "https://api.elevenlabs.io/v1/text-to-speech/abc123"
        assert call.kwargs["headers"]["xi-api-key"] == "el-test"
        assert call.kwargs["json"] == {"text": "Bonjour", "model_id": "eleven_multilingual_v2"}

        # The bytes ElevenLabs "returned" should actually be written to disk
        # and served back through the /audio static mount.
        served = client.get(audio_url.replace("http://localhost:8002", ""))
        assert served.status_code == 200
        assert served.content == b"fake-mp3-bytes"


def test_synthesize_returns_502_when_elevenlabs_unreachable():
    with patch("app.main.settings") as mock_settings, patch("httpx.post") as mock_post:
        mock_settings.elevenlabs_api_key = "el-test"
        mock_settings.elevenlabs_base_url = "https://api.elevenlabs.io/v1/text-to-speech"
        mock_settings.elevenlabs_model_id = "eleven_multilingual_v2"
        mock_settings.supported_languages = ("de", "fr", "es", "ta", "te", "kn")
        import httpx

        mock_post.side_effect = httpx.ConnectError("connection refused")

        response = client.post(
            "/synthesize", json={"text": "hi", "language": "de", "voice_id": "abc123"}
        )
        assert response.status_code == 502
