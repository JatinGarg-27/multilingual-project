"""Provider-agnostic LLM service.

Points at whichever LLM API is configured via LLM_API_BASE_URL / LLM_API_KEY.
Swap providers by changing env vars only — callers never touch this detail.
"""

import httpx

from app.core.config import settings


class LLMService:
    def __init__(self) -> None:
        self.base_url = settings.llm_api_base_url
        self.api_key = settings.llm_api_key
        self.model = settings.llm_model or "default"

    def _configured(self) -> bool:
        return bool(self.base_url and self.api_key)

    def _call(self, prompt: str) -> str:
        if not self._configured():
            return f"[stub output — no LLM_API_BASE_URL/LLM_API_KEY set]\n{prompt}"

        response = httpx.post(
            self.base_url,
            headers={"Authorization": f"Bearer {self.api_key}"},
            json={"model": self.model, "prompt": prompt},
            timeout=30.0,
        )
        response.raise_for_status()
        return response.json()["output"]

    def generate_draft(self, prompt: str) -> str:
        return self._call(prompt)

    def refine(self, content: str, instructions: str) -> str:
        prompt = f"Refine the following content.\n\nInstructions: {instructions}\n\nContent:\n{content}"
        return self._call(prompt)


llm_service = LLMService()
