"""HTTP client for the generation-service (owns the LLM API integration)."""

import httpx
from fastapi import HTTPException

from app.core.config import settings


def _post(path: str, json: dict) -> dict:
    try:
        response = httpx.post(f"{settings.generation_service_url}{path}", json=json, timeout=30.0)
        response.raise_for_status()
    except httpx.HTTPStatusError as exc:
        raise HTTPException(
            status_code=502, detail=f"generation-service error: {exc.response.text}"
        ) from exc
    except httpx.RequestError as exc:
        raise HTTPException(status_code=502, detail=f"generation-service unreachable: {exc}") from exc
    return response.json()


class GenerationClient:
    def generate_draft(self, prompt: str) -> dict:
        return _post("/generate", {"prompt": prompt})

    def refine(self, content: str, instructions: str) -> dict:
        return _post("/refine", {"content": content, "instructions": instructions})


generation_client = GenerationClient()
