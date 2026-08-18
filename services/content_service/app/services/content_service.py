import uuid

from fastapi import HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.content import Content
from app.models.generation import GenerationHistory
from app.models.user import User


def next_version(db: Session, content_id: uuid.UUID) -> int:
    current_max = db.scalar(
        select(func.max(GenerationHistory.version)).where(GenerationHistory.content_id == content_id)
    )
    return (current_max or 0) + 1


def get_owned_content(db: Session, user: User, content_id: uuid.UUID) -> Content:
    content = db.get(Content, content_id)
    if content is None or content.owner_id != user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Content not found")
    return content
