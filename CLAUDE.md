# Project Rules

## Architecture
Microservice-oriented backend, three independently deployable/scalable/testable services under `services/`:

- `content_service/` — owns Postgres persistence (users, contents, generation_history, voice_preferences, audio_assets), auth (JWT), and the public REST API (`/api/v1/...`). Orchestrates calls to the other two services over HTTP.
- `generation_service/` — owns the LLM API integration (Google Gemini: `POST /generate`, `POST /refine`). Stateless, no DB.
- `tts_service/` — owns the TTS integration (gTTS / Google Translate TTS: `POST /synthesize`, `GET /languages`, `GET /voices/{language}`), covering German, French, Spanish, Tamil, Telugu, Kannada — gTTS genuinely supports all six, needs no API key or account. Generated audio is written to `audio_output/` and served back via a `/audio` static mount. Stateless (no DB of its own). See DECISION-007 in `DECISION_LOG.md` for why this replaced OpenAI/ElevenLabs.

Each service has its own `requirements.txt`, `Dockerfile`, `.env.example`, and `tests/`, and can be built, deployed, and scaled independently. `content_service` calls the other two over plain HTTP (`httpx`), configured via `GENERATION_SERVICE_URL` / `TTS_SERVICE_URL`.

## Stack
- Language: Python 3.12
- Framework: FastAPI
- Database: PostgreSQL via SQLAlchemy 2.0 + Alembic migrations (content_service only)
- LLM API: Google Gemini (free tier, no card required), behind generation_service's `_call_llm`
- TTS: gTTS / Google Translate TTS (free, no API key), behind tts_service's `_call_gtts`

## Conventions
- Use Conventional Commits (feat:, fix:, docs:, chore:, refactor:, test:)
- Every significant AI-driven or architectural change must be recorded in `DECISION_LOG.md` before/after the change, per that file's own protocol
- Business logic goes in each service's `app/services/`, not in route handlers
- Every DB schema change goes through an Alembic migration, never hand-edited
- Cross-service calls always go through the HTTP client in `content_service/app/services/{generation_client,tts_client}.py` — never import another service's code directly

## Layout
```
services/
  content_service/
    app/{main,core,db,models,schemas,api,services}
    alembic/
    tests/
  generation_service/
    app/{main,config}
    tests/
  tts_service/
    app/{main,config}
    tests/
docker-compose.yml   # db + all three services
```
