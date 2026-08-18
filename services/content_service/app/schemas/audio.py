import uuid
from datetime import datetime

from pydantic import BaseModel


class SpeechRequest(BaseModel):
    language: str
    voice_id: str | None = None


class AudioAssetOut(BaseModel):
    id: uuid.UUID
    content_id: uuid.UUID
    language: str
    voice_id: str
    status: str
    audio_url: str | None
    created_at: datetime

    class Config:
        from_attributes = True
