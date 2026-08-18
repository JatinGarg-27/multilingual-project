import uuid

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.models.generation import GenerationHistory
from app.models.user import User
from app.schemas.generation import GenerateRequest, GenerationOut, RefineRequest
from app.services.content_service import get_owned_content, next_version
from app.services.llm_service import llm_service

router = APIRouter(prefix="/content/{content_id}", tags=["generation"])


@router.post("/generate", response_model=GenerationOut, status_code=201)
def generate(
    content_id: uuid.UUID,
    payload: GenerateRequest,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> GenerationHistory:
    content = get_owned_content(db, user, content_id)
    output = llm_service.generate_draft(payload.prompt)

    entry = GenerationHistory(
        content_id=content.id,
        version=next_version(db, content.id),
        action="generate",
        prompt=payload.prompt,
        model=llm_service.model,
        output=output,
    )
    content.body = output
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry


@router.post("/refine", response_model=GenerationOut, status_code=201)
def refine(
    content_id: uuid.UUID,
    payload: RefineRequest,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> GenerationHistory:
    content = get_owned_content(db, user, content_id)
    output = llm_service.refine(content.body, payload.instructions)

    entry = GenerationHistory(
        content_id=content.id,
        version=next_version(db, content.id),
        action="refine",
        prompt=payload.instructions,
        model=llm_service.model,
        output=output,
    )
    content.body = output
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry


@router.get("/history", response_model=list[GenerationOut])
def get_history(
    content_id: uuid.UUID, db: Session = Depends(get_db), user: User = Depends(get_current_user)
) -> list[GenerationHistory]:
    content = get_owned_content(db, user, content_id)
    stmt = (
        select(GenerationHistory)
        .where(GenerationHistory.content_id == content.id)
        .order_by(GenerationHistory.version)
    )
    return list(db.scalars(stmt))
