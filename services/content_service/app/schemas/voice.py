import uuid

from pydantic import BaseModel


class VoicePreferenceCreate(BaseModel):
    language: str
    voice_id: str


class VoicePreferenceOut(BaseModel):
    id: uuid.UUID
    language: str
    voice_id: str

    class Config:
        from_attributes = True
