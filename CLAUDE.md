# Project Rules

## Stack
- Language: Python 3.12
- Framework: FastAPI
- Database: PostgreSQL via SQLAlchemy 2.0 + Alembic migrations
- LLM API: pluggable provider behind an `llm_service` abstraction
- TTS API: pluggable provider behind a `tts_service` abstraction, covering German, French, Spanish, Tamil, Telugu, Kannada
- Package management: `requirements.txt` / `requirements-dev.txt`, virtualenv

## Conventions
- Use Conventional Commits (feat:, fix:, docs:, chore:, refactor:, test:)
- All endpoints live under `/api/v1/`
- Every significant AI-driven or architectural change must be recorded in `DECISION_LOG.md` before/after the change, per that file's own protocol
- Business logic goes in `app/services/`, not in route handlers
- Every DB schema change goes through an Alembic migration, never hand-edited

## Layout
```
app/
  main.py
  core/       # config, security
  db/         # session, base
  models/     # SQLAlchemy models
  schemas/    # Pydantic schemas
  api/v1/     # routers
  services/   # llm_service, tts_service, content_service
alembic/
tests/
```
