"""generation-service — owns the LLM API integration.

Independently deployable so it can scale separately from content
persistence and TTS conversion, and be tested in isolation.
"""

import httpx
from fastapi import FastAPI
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
    return bool(settings.llm_api_base_url and settings.llm_api_key)


def _call_llm(prompt: str) -> str:
    if not _configured():
        return f"[stub output — no LLM_API_BASE_URL/LLM_API_KEY set]\n{prompt}"

    response = httpx.post(
        settings.llm_api_base_url,
        headers={"Authorization": f"Bearer {settings.llm_api_key}"},
        json={"model": settings.llm_model, "prompt": prompt},
        timeout=30.0,
    )
    response.raise_for_status()
    return response.json()["output"]


@app.post("/generate", response_model=GenerationOut)
def generate(payload: GenerateRequest) -> GenerationOut:
    output = _call_llm(payload.prompt)
    return GenerationOut(output=output, model=settings.llm_model)


@app.post("/refine", response_model=GenerationOut)
def refine(payload: RefineRequest) -> GenerationOut:
    prompt = f"Refine the following content.\n\nInstructions: {payload.instructions}\n\nContent:\n{payload.content}"
    output = _call_llm(prompt)
    return GenerationOut(output=output, model=settings.llm_model)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
