# Multilingual AI Content & TTS Copilot (Backend)

Python, FastAPI, PostgreSQL, REST APIs, LLM API, TTS API

A backend service that powers Copilot-style content generation and operational workflows for content teams, exposing RESTful APIs for content creation, editing, and retrieval.

Integrates an LLM API to draft and refine content, paired with a TTS API to convert content into natural speech across European (German, French, Spanish) and Indian regional languages (Tamil, Telugu, Kannada).

Uses a PostgreSQL-backed data layer to persist content, generation history, and per-language voice preferences, with clean, versioned API contracts for downstream use.

Structured with a modular, microservice-oriented architecture so generation, TTS conversion, and persistence layers can scale and be tested independently — see [CLAUDE.md](CLAUDE.md) for the service breakdown.

## Providers

- LLM: Google Gemini — free tier, no card required. Get a key at [aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey).
- TTS: gTTS (Google Translate TTS) — completely free, no API key or account needed, and genuinely covers all six languages including Telugu and Kannada. See DECISION-007 in [DECISION_LOG.md](DECISION_LOG.md) for why this replaced OpenAI/ElevenLabs.

## Running locally

```bash
docker compose up --build
```

This starts Postgres, `generation-service` (:8001), `tts-service` (:8002), and `content-service` (:8000, the public API — docs at `/docs`). Copy each service's `.env.example` to `.env` first, and fill in `GEMINI_API_KEY` (generation_service only — tts_service needs no key at all) to get real drafted text instead of stub responses.

## Try it without an API client

`http://localhost:8000/demo/` is a small interactive page — draft content with AI, edit it, pick a language, and hear it spoken back — for anyone who'd rather not use `/docs` directly. Auth is handled silently in the background.

## Decision log
Every significant architectural or AI-driven change is recorded in [DECISION_LOG.md](DECISION_LOG.md).
