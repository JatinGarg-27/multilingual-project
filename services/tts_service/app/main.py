"""tts-service — owns the TTS integration.

Uses gTTS (Google Translate's text-to-speech), which is free and needs no
API key or account — unlike ElevenLabs, it also genuinely supports all six
required languages (German, French, Spanish, Tamil, Telugu, Kannada).
See DECISION-007 in DECISION_LOG.md for why this replaced ElevenLabs.

Independently deployable so it can scale separately from content
persistence and LLM generation, and be tested in isolation.
"""

import io
import uuid
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from gtts import gTTS
from gtts.tts import gTTSError
from pydantic import BaseModel

from app.config import settings

STORAGE_DIR = Path(settings.audio_storage_dir)
STORAGE_DIR.mkdir(parents=True, exist_ok=True)

app = FastAPI(title="TTS service")
app.mount("/audio", StaticFiles(directory=str(STORAGE_DIR)), name="audio")


class SynthesizeRequest(BaseModel):
    text: str
    language: str
    # Not used by gTTS (it has no concept of selectable voices) — kept so
    # content-service's existing request shape doesn't need to change.
    voice_id: str = ""


class SynthesizeOut(BaseModel):
    audio_url: str


class VoiceOut(BaseModel):
    language: str
    voice_id: str


@app.get("/languages", response_model=list[str])
def list_languages() -> list[str]:
    return list(settings.supported_languages)


@app.get("/voices/{language}", response_model=VoiceOut)
def default_voice(language: str) -> VoiceOut:
    if language not in settings.supported_languages:
        raise HTTPException(status_code=400, detail=f"Unsupported language: {language}")
    return VoiceOut(language=language, voice_id="gtts-default")


def _call_gtts(text: str, language: str) -> bytes:
    try:
        tts = gTTS(text=text, lang=language)
        buf = io.BytesIO()
        tts.write_to_fp(buf)
        return buf.getvalue()
    except gTTSError as exc:
        raise HTTPException(status_code=502, detail=f"TTS provider error: {exc}") from exc
    except Exception as exc:  # network errors etc. from the underlying HTTP call
        raise HTTPException(status_code=502, detail=f"TTS provider unreachable: {exc}") from exc


@app.post("/synthesize", response_model=SynthesizeOut)
def synthesize(payload: SynthesizeRequest) -> SynthesizeOut:
    if payload.language not in settings.supported_languages:
        raise HTTPException(status_code=400, detail=f"Unsupported language: {payload.language}")

    audio_bytes = _call_gtts(payload.text, payload.language)

    filename = f"{uuid.uuid4()}.mp3"
    (STORAGE_DIR / filename).write_bytes(audio_bytes)

    return SynthesizeOut(audio_url=f"{settings.public_base_url}/audio/{filename}")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
