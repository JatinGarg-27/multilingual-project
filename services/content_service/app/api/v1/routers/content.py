import uuid

from fastapi import APIRouter, Depends, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.models.content import Content
from app.models.user import User
from app.schemas.content import ContentCreate, ContentOut, ContentUpdate
from app.services.content_service import get_owned_content

router = APIRouter(prefix="/content", tags=["content"])


@router.post("", response_model=ContentOut, status_code=status.HTTP_201_CREATED)
def create_content(
    payload: ContentCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)
) -> Content:
    content = Content(title=payload.title, body=payload.body, owner_id=user.id)
    db.add(content)
    db.commit()
    db.refresh(content)
    return content


@router.get("", response_model=list[ContentOut])
def list_content(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
    limit: int = 20,
    offset: int = 0,
) -> list[Content]:
    stmt = select(Content).where(Content.owner_id == user.id).limit(limit).offset(offset)
    return list(db.scalars(stmt))


@router.get("/{content_id}", response_model=ContentOut)
def get_content(
    content_id: uuid.UUID, db: Session = Depends(get_db), user: User = Depends(get_current_user)
) -> Content:
    return get_owned_content(db, user, content_id)


@router.patch("/{content_id}", response_model=ContentOut)
def update_content(
    content_id: uuid.UUID,
    payload: ContentUpdate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> Content:
    content = get_owned_content(db, user, content_id)
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(content, field, value)
    db.commit()
    db.refresh(content)
    return content


@router.delete("/{content_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_content(
    content_id: uuid.UUID, db: Session = Depends(get_db), user: User = Depends(get_current_user)
) -> None:
    content = get_owned_content(db, user, content_id)
    db.delete(content)
    db.commit()
