from unittest.mock import patch

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


def test_synthesize_rejects_unsupported_language():
    response = client.post(
        "/synthesize", json={"text": "hi", "language": "xx", "voice_id": "v1"}
    )
    assert response.status_code == 400


def test_synthesize_calls_gtts_and_serves_the_file():
    with patch("app.main._call_gtts") as mock_call:
        mock_call.return_value = b"fake-mp3-bytes"

        response = client.post(
            "/synthesize", json={"text": "Bonjour", "language": "fr", "voice_id": ""}
        )

        assert response.status_code == 200
        audio_url = response.json()["audio_url"]
        assert audio_url.endswith(".mp3")

        mock_call.assert_called_once_with("Bonjour", "fr")

        served = client.get(audio_url.replace("http://localhost:8002", ""))
        assert served.status_code == 200
        assert served.content == b"fake-mp3-bytes"


def test_synthesize_returns_502_when_gtts_fails():
    with patch("app.main._call_gtts") as mock_call:
        from fastapi import HTTPException

        mock_call.side_effect = HTTPException(status_code=502, detail="TTS provider unreachable: boom")

        response = client.post(
            "/synthesize", json={"text": "hi", "language": "de", "voice_id": ""}
        )
        assert response.status_code == 502


def test_synthesize_covers_telugu_and_kannada_end_to_end():
    """Unlike ElevenLabs, gTTS genuinely supports these two — verify both are wired up, not just German/French/Spanish."""
    with patch("app.main._call_gtts") as mock_call:
        mock_call.return_value = b"fake-mp3-bytes"
        for lang in ("te", "kn"):
            response = client.post(
                "/synthesize", json={"text": "test", "language": lang, "voice_id": ""}
            )
            assert response.status_code == 200
