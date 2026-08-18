"""Provider-agnostic TTS service.

Points at whichever TTS API is configured via TTS_API_BASE_URL / TTS_API_KEY.
Covers German (de), French (fr), Spanish (es), Tamil (ta), Telugu (te), Kannada (kn).
"""

import uuid

import httpx

from app.core.config import settings

DEFAULT_VOICES = {
    "de": "default-de",
    "fr": "default-fr",
    "es": "default-es",
    "ta": "default-ta",
    "te": "default-te",
    "kn": "default-kn",
}


class UnsupportedLanguageError(ValueError):
    pass


class TTSService:
    def __init__(self) -> None:
        self.base_url = settings.tts_api_base_url
        self.api_key = settings.tts_api_key

    def _configured(self) -> bool:
        return bool(self.base_url and self.api_key)

    def default_voice_for(self, language: str) -> str:
        if language not in settings.supported_languages:
            raise UnsupportedLanguageError(f"Unsupported language: {language}")
        return DEFAULT_VOICES[language]

    def synthesize(self, text: str, language: str, voice_id: str) -> str:
        """Returns a URL to the generated audio asset."""
        if language not in settings.supported_languages:
            raise UnsupportedLanguageError(f"Unsupported language: {language}")

        if not self._configured():
            return f"stub://audio/{uuid.uuid4()}.mp3"

        response = httpx.post(
            self.base_url,
            headers={"Authorization": f"Bearer {self.api_key}"},
            json={"text": text, "language": language, "voice_id": voice_id},
            timeout=60.0,
        )
        response.raise_for_status()
        return response.json()["audio_url"]


tts_service = TTSService()
