from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from app.api.v1.router import api_router
from app.services.tts_client import UnsupportedLanguageError

app = FastAPI(title="Multilingual AI Content & TTS Copilot — content service")

app.include_router(api_router)

STATIC_DIR = Path(__file__).resolve().parent.parent / "static"
app.mount("/demo", StaticFiles(directory=str(STATIC_DIR), html=True), name="demo")


@app.exception_handler(UnsupportedLanguageError)
def unsupported_language_handler(request: Request, exc: UnsupportedLanguageError) -> JSONResponse:
    return JSONResponse(status_code=400, content={"detail": str(exc)})


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
