"""generation-service — owns the LLM API integration (OpenAI Chat Completions).

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
    return bool(settings.openai_api_key)


def _call_llm(prompt: str) -> str:
    if not _configured():
        return f"[stub output — no OPENAI_API_KEY set]\n{prompt}"

    try:
        response = httpx.post(
            settings.openai_base_url,
            headers={
                "Authorization": f"Bearer {settings.openai_api_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": settings.openai_model,
                "messages": [{"role": "user", "content": prompt}],
            },
            timeout=30.0,
        )
        response.raise_for_status()
    except httpx.HTTPStatusError as exc:
        raise HTTPException(
            status_code=502, detail=f"LLM provider error: {exc.response.status_code} {exc.response.text}"
        ) from exc
    except httpx.RequestError as exc:
        raise HTTPException(status_code=502, detail=f"LLM provider unreachable: {exc}") from exc

    return response.json()["choices"][0]["message"]["content"]


@app.post("/generate", response_model=GenerationOut)
def generate(payload: GenerateRequest) -> GenerationOut:
    output = _call_llm(payload.prompt)
    return GenerationOut(output=output, model=settings.openai_model)


@app.post("/refine", response_model=GenerationOut)
def refine(payload: RefineRequest) -> GenerationOut:
    prompt = f"Refine the following content.\n\nInstructions: {payload.instructions}\n\nContent:\n{payload.content}"
    output = _call_llm(prompt)
    return GenerationOut(output=output, model=settings.openai_model)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
