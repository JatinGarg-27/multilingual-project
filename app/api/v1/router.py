from fastapi import APIRouter

from app.api.v1.routers import auth, content, generation, speech, voices

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(auth.router)
api_router.include_router(content.router)
api_router.include_router(generation.router)
api_router.include_router(speech.router)
api_router.include_router(voices.router)
