# Multilingual AI Content & TTS Copilot (Backend)

Python, FastAPI, PostgreSQL, REST APIs, LLM API, TTS API

A backend service that powers Copilot-style content generation and operational workflows for content teams, exposing RESTful APIs for content creation, editing, and retrieval.

Integrates an LLM API to draft and refine content, paired with a TTS API to convert content into natural speech across European (German, French, Spanish) and Indian regional languages (Tamil, Telugu, Kannada).

Uses a PostgreSQL-backed data layer to persist content, generation history, and per-language voice preferences, with clean, versioned API contracts for downstream use.

Structured with a modular, microservice-oriented architecture so generation, TTS conversion, and persistence layers can scale and be tested independently — see [CLAUDE.md](CLAUDE.md) for the service breakdown.

## Providers

- LLM: OpenAI (Chat Completions)
- TTS: ElevenLabs — note: Telugu and Kannada are accepted by the API but not officially supported by ElevenLabs' multilingual model; see DECISION-004 in [DECISION_LOG.md](DECISION_LOG.md).

## Running locally

```bash
docker compose up --build
```

This starts Postgres, `generation-service` (:8001), `tts-service` (:8002), and `content-service` (:8000, the public API — docs at `/docs`). Copy each service's `.env.example` to `.env` first, and fill in `OPENAI_API_KEY` (generation_service) and `ELEVENLABS_API_KEY` (tts_service) to get real output instead of stub responses.

## Decision log
Every significant architectural or AI-driven change is recorded in [DECISION_LOG.md](DECISION_LOG.md).
