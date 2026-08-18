"""HTTP client for the tts-service (owns the TTS API integration)."""

import httpx

from app.core.config import settings


class UnsupportedLanguageError(ValueError):
    pass


class TTSClient:
    def default_voice_for(self, language: str) -> str:
        response = httpx.get(f"{settings.tts_service_url}/voices/{language}", timeout=10.0)
        if response.status_code == 400:
            raise UnsupportedLanguageError(response.json().get("detail", f"Unsupported language: {language}"))
        response.raise_for_status()
        return response.json()["voice_id"]

    def synthesize(self, text: str, language: str, voice_id: str) -> str:
        response = httpx.post(
            f"{settings.tts_service_url}/synthesize",
            json={"text": text, "language": language, "voice_id": voice_id},
            timeout=60.0,
        )
        if response.status_code == 400:
            raise UnsupportedLanguageError(response.json().get("detail", f"Unsupported language: {language}"))
        response.raise_for_status()
        return response.json()["audio_url"]


tts_client = TTSClient()
