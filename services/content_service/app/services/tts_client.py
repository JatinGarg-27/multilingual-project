"""HTTP client for the tts-service (owns the TTS API integration)."""

import httpx
from fastapi import HTTPException

from app.core.config import settings


class UnsupportedLanguageError(ValueError):
    pass


def _handle_error_response(response: httpx.Response, language: str) -> None:
    if response.status_code == 400:
        raise UnsupportedLanguageError(response.json().get("detail", f"Unsupported language: {language}"))
    if response.status_code >= 400:
        raise HTTPException(status_code=502, detail=f"tts-service error: {response.text}")


class TTSClient:
    def default_voice_for(self, language: str) -> str:
        try:
            response = httpx.get(f"{settings.tts_service_url}/voices/{language}", timeout=10.0)
        except httpx.RequestError as exc:
            raise HTTPException(status_code=502, detail=f"tts-service unreachable: {exc}") from exc
        _handle_error_response(response, language)
        return response.json()["voice_id"]

    def synthesize(self, text: str, language: str, voice_id: str) -> str:
        try:
            response = httpx.post(
                f"{settings.tts_service_url}/synthesize",
                json={"text": text, "language": language, "voice_id": voice_id},
                timeout=60.0,
            )
        except httpx.RequestError as exc:
            raise HTTPException(status_code=502, detail=f"tts-service unreachable: {exc}") from exc
        _handle_error_response(response, language)
        return response.json()["audio_url"]


tts_client = TTSClient()
