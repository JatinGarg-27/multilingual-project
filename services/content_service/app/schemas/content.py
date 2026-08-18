import uuid
from datetime import datetime

from pydantic import BaseModel


class ContentCreate(BaseModel):
    title: str
    body: str = ""


class ContentUpdate(BaseModel):
    title: str | None = None
    body: str | None = None
    status: str | None = None


class ContentOut(BaseModel):
    id: uuid.UUID
    title: str
    body: str
    status: str
    owner_id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
