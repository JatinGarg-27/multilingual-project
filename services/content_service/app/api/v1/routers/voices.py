from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.core.config import settings
from app.models.user import User
from app.models.voice import VoicePreference
from app.schemas.voice import VoicePreferenceCreate, VoicePreferenceOut

router = APIRouter(prefix="/voices", tags=["voices"])


@router.get("/languages", response_model=list[str])
def list_supported_languages() -> list[str]:
    return list(settings.supported_languages)


@router.get("/preferences", response_model=list[VoicePreferenceOut])
def list_preferences(db: Session = Depends(get_db), user: User = Depends(get_current_user)) -> list[VoicePreference]:
    stmt = select(VoicePreference).where(VoicePreference.user_id == user.id)
    return list(db.scalars(stmt))


@router.put("/preferences", response_model=VoicePreferenceOut)
def set_preference(
    payload: VoicePreferenceCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)
) -> VoicePreference:
    existing = db.scalar(
        select(VoicePreference).where(
            VoicePreference.user_id == user.id, VoicePreference.language == payload.language
        )
    )
    if existing:
        existing.voice_id = payload.voice_id
        db.commit()
        db.refresh(existing)
        return existing

    pref = VoicePreference(user_id=user.id, language=payload.language, voice_id=payload.voice_id)
    db.add(pref)
    db.commit()
    db.refresh(pref)
    return pref
