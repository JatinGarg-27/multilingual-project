"""tts-service — owns the TTS API integration.

Independently deployable so it can scale separately from content
persistence and LLM generation, and be tested in isolation.
Covers German (de), French (fr), Spanish (es), Tamil (ta), Telugu (te), Kannada (kn).
"""

import uuid

import httpx
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from app.config import settings

app = FastAPI(title="TTS service")

DEFAULT_VOICES = {
    "de": "default-de",
    "fr": "default-fr",
    "es": "default-es",
    "ta": "default-ta",
    "te": "default-te",
    "kn": "default-kn",
}


class SynthesizeRequest(BaseModel):
    text: str
    language: str
    voice_id: str


class SynthesizeOut(BaseModel):
    audio_url: str


class VoiceOut(BaseModel):
    language: str
    voice_id: str


def _configured() -> bool:
    return bool(settings.tts_api_base_url and settings.tts_api_key)


@app.get("/languages", response_model=list[str])
def list_languages() -> list[str]:
    return list(settings.supported_languages)


@app.get("/voices/{language}", response_model=VoiceOut)
def default_voice(language: str) -> VoiceOut:
    if language not in settings.supported_languages:
        raise HTTPException(status_code=400, detail=f"Unsupported language: {language}")
    return VoiceOut(language=language, voice_id=DEFAULT_VOICES[language])


@app.post("/synthesize", response_model=SynthesizeOut)
def synthesize(payload: SynthesizeRequest) -> SynthesizeOut:
    if payload.language not in settings.supported_languages:
        raise HTTPException(status_code=400, detail=f"Unsupported language: {payload.language}")

    if not _configured():
        return SynthesizeOut(audio_url=f"stub://audio/{uuid.uuid4()}.mp3")

    response = httpx.post(
        settings.tts_api_base_url,
        headers={"Authorization": f"Bearer {settings.tts_api_key}"},
        json={"text": payload.text, "language": payload.language, "voice_id": payload.voice_id},
        timeout=60.0,
    )
    response.raise_for_status()
    return SynthesizeOut(audio_url=response.json()["audio_url"])


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
