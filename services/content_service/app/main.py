from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.api.v1.router import api_router
from app.services.tts_client import UnsupportedLanguageError

app = FastAPI(title="Multilingual AI Content & TTS Copilot — content service")

app.include_router(api_router)


@app.exception_handler(UnsupportedLanguageError)
def unsupported_language_handler(request: Request, exc: UnsupportedLanguageError) -> JSONResponse:
    return JSONResponse(status_code=400, content={"detail": str(exc)})


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
