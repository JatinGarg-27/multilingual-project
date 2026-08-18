import uuid

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.models.audio import AudioAsset
from app.models.user import User
from app.schemas.audio import AudioAssetOut, SpeechRequest
from app.services.content_service import get_owned_content
from app.services.tts_client import tts_client

router = APIRouter(prefix="/content/{content_id}", tags=["speech"])


@router.post("/speech", response_model=AudioAssetOut, status_code=201)
def generate_speech(
    content_id: uuid.UUID,
    payload: SpeechRequest,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> AudioAsset:
    content = get_owned_content(db, user, content_id)
    voice_id = payload.voice_id or tts_client.default_voice_for(payload.language)

    audio_url = tts_client.synthesize(content.body, payload.language, voice_id)

    asset = AudioAsset(
        content_id=content.id,
        language=payload.language,
        voice_id=voice_id,
        status="completed",
        audio_url=audio_url,
    )
    db.add(asset)
    db.commit()
    db.refresh(asset)
    return asset
