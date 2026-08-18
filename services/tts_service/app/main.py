"""tts-service — owns the TTS API integration (ElevenLabs).

Independently deployable so it can scale separately from content
persistence and LLM generation, and be tested in isolation.
Covers German (de), French (fr), Spanish (es), Tamil (ta) — Telugu (te) and
Kannada (kn) are accepted but not officially supported by ElevenLabs'
multilingual model; see DECISION-004 in DECISION_LOG.md.
"""

import uuid
from pathlib import Path

import httpx
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from app.config import settings

STORAGE_DIR = Path(settings.audio_storage_dir)
STORAGE_DIR.mkdir(parents=True, exist_ok=True)

app = FastAPI(title="TTS service")
app.mount("/audio", StaticFiles(directory=str(STORAGE_DIR)), name="audio")


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
    return bool(settings.elevenlabs_api_key)


@app.get("/languages", response_model=list[str])
def list_languages() -> list[str]:
    return list(settings.supported_languages)


@app.get("/voices/{language}", response_model=VoiceOut)
def default_voice(language: str) -> VoiceOut:
    if language not in settings.supported_languages:
        raise HTTPException(status_code=400, detail=f"Unsupported language: {language}")
    return VoiceOut(language=language, voice_id=settings.default_voice_id)


def _call_elevenlabs(text: str, voice_id: str) -> bytes:
    try:
        response = httpx.post(
            f"{settings.elevenlabs_base_url}/{voice_id}",
            headers={
                "xi-api-key": settings.elevenlabs_api_key,
                "Content-Type": "application/json",
                "Accept": "audio/mpeg",
            },
            json={"text": text, "model_id": settings.elevenlabs_model_id},
            timeout=60.0,
        )
        response.raise_for_status()
    except httpx.HTTPStatusError as exc:
        raise HTTPException(
            status_code=502, detail=f"TTS provider error: {exc.response.status_code} {exc.response.text}"
        ) from exc
    except httpx.RequestError as exc:
        raise HTTPException(status_code=502, detail=f"TTS provider unreachable: {exc}") from exc

    return response.content


@app.post("/synthesize", response_model=SynthesizeOut)
def synthesize(payload: SynthesizeRequest) -> SynthesizeOut:
    if payload.language not in settings.supported_languages:
        raise HTTPException(status_code=400, detail=f"Unsupported language: {payload.language}")

    if not _configured():
        return SynthesizeOut(audio_url=f"stub://audio/{uuid.uuid4()}.mp3")

    audio_bytes = _call_elevenlabs(payload.text, payload.voice_id)

    filename = f"{uuid.uuid4()}.mp3"
    (STORAGE_DIR / filename).write_bytes(audio_bytes)

    return SynthesizeOut(audio_url=f"{settings.public_base_url}/audio/{filename}")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
