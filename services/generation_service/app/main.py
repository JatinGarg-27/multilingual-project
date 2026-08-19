"""generation-service — owns the LLM API integration (Google Gemini, free tier).

Independently deployable so it can scale separately from content
persistence and TTS conversion, and be tested in isolation.
"""

import httpx
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from app.config import settings

app = FastAPI(title="Generation service")


class GenerateRequest(BaseModel):
    prompt: str


class RefineRequest(BaseModel):
    content: str
    instructions: str


class GenerationOut(BaseModel):
    output: str
    model: str


def _configured() -> bool:
    return bool(settings.gemini_api_key)


def _call_llm(prompt: str) -> str:
    if not _configured():
        return f"[stub output — no GEMINI_API_KEY set]\n{prompt}"

    url = f"{settings.gemini_base_url}/{settings.gemini_model}:generateContent"
    try:
        response = httpx.post(
            url,
            params={"key": settings.gemini_api_key},
            json={"contents": [{"parts": [{"text": prompt}]}]},
            timeout=30.0,
        )
        response.raise_for_status()
    except httpx.HTTPStatusError as exc:
        raise HTTPException(
            status_code=502, detail=f"LLM provider error: {exc.response.status_code} {exc.response.text}"
        ) from exc
    except httpx.RequestError as exc:
        raise HTTPException(status_code=502, detail=f"LLM provider unreachable: {exc}") from exc

    data = response.json()
    return data["candidates"][0]["content"]["parts"][0]["text"]


@app.post("/generate", response_model=GenerationOut)
def generate(payload: GenerateRequest) -> GenerationOut:
    output = _call_llm(payload.prompt)
    return GenerationOut(output=output, model=settings.gemini_model)


@app.post("/refine", response_model=GenerationOut)
def refine(payload: RefineRequest) -> GenerationOut:
    prompt = f"Refine the following content.\n\nInstructions: {payload.instructions}\n\nContent:\n{payload.content}"
    output = _call_llm(prompt)
    return GenerationOut(output=output, model=settings.gemini_model)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
