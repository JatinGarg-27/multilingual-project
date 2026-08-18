"""HTTP client for the generation-service (owns the LLM API integration)."""

import httpx

from app.core.config import settings


class GenerationClient:
    def generate_draft(self, prompt: str) -> dict:
        response = httpx.post(
            f"{settings.generation_service_url}/generate", json={"prompt": prompt}, timeout=30.0
        )
        response.raise_for_status()
        return response.json()

    def refine(self, content: str, instructions: str) -> dict:
        response = httpx.post(
            f"{settings.generation_service_url}/refine",
            json={"content": content, "instructions": instructions},
            timeout=30.0,
        )
        response.raise_for_status()
        return response.json()


generation_client = GenerationClient()
