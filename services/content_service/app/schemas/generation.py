import uuid
from datetime import datetime

from pydantic import BaseModel


class GenerateRequest(BaseModel):
    prompt: str


class RefineRequest(BaseModel):
    instructions: str


class GenerationOut(BaseModel):
    id: uuid.UUID
    content_id: uuid.UUID
    version: int
    action: str
    prompt: str
    model: str
    output: str
    created_at: datetime

    class Config:
        from_attributes = True
