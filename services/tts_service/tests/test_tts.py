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
    assert response.json() == {"language": "ta", "voice_id": "default-ta"}


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
