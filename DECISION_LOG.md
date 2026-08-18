# Decision Log

> **Purpose:** This file records every meaningful modification made to the project, especially modifications made by AI.  
> **Rule:** Never modify the project without recording the reason and decision here.

---

## How AI Must Use This File

Before making a significant modification:

1. Understand the current implementation.
2. Identify the problem, requirement, error, or reason for change.
3. Explain what is currently happening.
4. Decide what should change.
5. Record the decision in this file.
6. Make the code changes.
7. Record the actual files/components modified.
8. Record the final result and any trade-offs.

### Important Rules

- **Do not record changes that were not actually made.**
- **Do not claim a fix works unless it was tested.**
- If a change was made because of an error, include the error.
- If a change was made because of a requirement, include the requirement.
- If the AI chose one approach over another, explain why.
- If an existing implementation was intentionally preserved, explain why.
- Never silently change architecture, dependencies, APIs, database structure, or major logic.
- Small formatting changes do not need an entry unless they affect behavior.
- Each decision must have a unique ID.
- Keep entries chronological, newest entry at the bottom.
- If a previous decision becomes invalid, do not delete it. Add a new decision explaining why it changed.

---

# Decision Entry Format

## DECISION-001 — [Short Title]

**Date:** YYYY-MM-DD  
**Status:** Accepted / Rejected / Superseded  
**Type:** Bug Fix / Feature / Refactor / Architecture / Security / Performance / Dependency / Configuration / UI / Database / Other

### 1. Trigger

What caused this change?

Examples:

- User requirement
- Bug/error
- Failed test
- Performance issue
- Security concern
- Better architecture
- Dependency limitation
- AI recommendation

### 2. Problem

What was wrong with the previous implementation?

Describe the actual behavior, not the desired behavior.

### 3. Previous Implementation

Explain how the project worked before this change.

```text
Example:

Frontend
   ↓
POST /api/resume
   ↓
Backend receives PDF
   ↓
Python script extracts text
   ↓
Claude generates LaTeX
```

### 4. Decision

What was changed?

Be specific.

- What logic changed?
- What architecture changed?
- What API changed?
- What dependency changed?
- What files were affected?

### 5. Why This Decision?

Explain the reasoning.

Include:

- Why this approach was selected
- Why the previous approach was insufficient
- Important constraints
- Expected benefits

### 6. Alternatives Considered

#### Alternative A

**Approach:**  
...

**Why rejected:**  
...

#### Alternative B

**Approach:**  
...

**Why rejected:**  
...

### 7. Files Modified

| File | Change | Reason |
|---|---|---|
| `backend/server.js` | Added error handling | Prevent server crashes |
| `backend/services/resume.js` | Changed processing flow | Support new resume pipeline |
| `frontend/src/App.jsx` | Updated API request | Match backend API |

### 8. Dependencies / Configuration

List anything added, removed, or changed.

```text
Added:
- package-name

Removed:
- package-name

Environment variables:
- NEW_VARIABLE

Configuration:
- Changed X → Y
```

### 9. Result

What happened after implementing the decision?

Include:

- Tests performed
- Expected behavior
- Actual behavior
- Remaining issues

Example:

```text
Test:
Uploaded resume.pdf with a Business Analyst JD.

Expected:
Tailored PDF should be generated.

Actual:
PDF generated successfully.

Status:
PASS
```

### 10. Trade-offs / Risks

What did we sacrifice or introduce?

Examples:

- More complexity
- Higher memory usage
- Additional dependency
- More API calls
- Slower processing
- Easier maintenance
- Better scalability

### 11. Rollback

How can this decision be reversed if necessary?

```text
Revert:
- Remove X
- Restore Y
- Revert commit: <commit-hash>
```

### 12. AI Reasoning Summary

Write a short explanation in plain English:

> The AI made this change because ________.  
> The previous implementation ________.  
> The new implementation ________.  
> This was preferred over ________ because ________.

---

# Project Decision History

<!--
Add every significant decision below.
Never delete previous decisions.
-->

## DECISION-001 — Scaffold Python/FastAPI backend, replacing Node.js template boilerplate

**Date:** 2026-08-18  
**Status:** Accepted  
**Type:** Architecture

### 1. Trigger

User requirement: build the "Multilingual AI Content & TTS Copilot (Backend)" project described on their resume (Python, FastAPI, PostgreSQL, REST APIs, LLM API, TTS API), and explicitly asked the AI to build it now.

### 2. Problem

The repo (`github.com/JatinGarg-27/multilingual-project`) contained only unedited capstone-project template boilerplate: `CLAUDE.md` declared `Stack: Node.js`, and `README.md` was a generic garbled placeholder ("Built with Node.js as part of my capstone project at [institution/program name]"). Neither reflected the actual project. There was no application code, no data layer, and no `DECISION_LOG.md` inside the repo (the governance file lived only on the Desktop, outside any repo).

### 3. Previous Implementation

```text
multilingual-project/
├── .gitignore   (garbled placeholder, "node_modules/")
├── CLAUDE.md    ("Stack: Node.js")
├── LICENSE
└── README.md    (garbled Node.js capstone template)
```

No backend code existed.

### 4. Decision

- Confirmed with the user that the real stack is Python/FastAPI/PostgreSQL (not Node.js) before writing any code — see Alternatives.
- Rewrote `CLAUDE.md` and `README.md` to describe the actual project, mirroring the resume's own wording (kept LLM/TTS provider references generic, per explicit user feedback not to invent specific vendor names).
- Fixed `.gitignore` (was also garbled/wrong-language boilerplate).
- Scaffolded a modular FastAPI app: `app/core` (config, security/JWT), `app/db` (SQLAlchemy session/base), `app/models` (User, Content, GenerationHistory, VoicePreference, AudioAsset), `app/schemas` (Pydantic request/response models), `app/services` (`llm_service`, `tts_service`, `content_service`), `app/api/v1/routers` (auth, content, generation, speech, voices).
- `llm_service` and `tts_service` are provider-agnostic: they call whatever HTTP endpoint is set in `LLM_API_BASE_URL`/`TTS_API_BASE_URL`, and fall back to a stub response when unconfigured. No specific LLM/TTS vendor was hardcoded, since the resume bullet and user both specified only "LLM API"/"TTS API" generically.
- Added Alembic migrations (initial schema for all 5 tables), Dockerfile + docker-compose.yml (api + Postgres), `.env.example`, and a pytest suite covering register/login, content CRUD, LLM generation history, and TTS language validation.
- Copied the user's Decision Log template into the repo root as `DECISION_LOG.md` so it travels with the code (previously it only existed on the Desktop, outside any repo).

### 5. Why This Decision?

- The Node.js declaration in `CLAUDE.md` was leftover template text, not a deliberate choice — confirmed directly with the user before overriding it, rather than assuming.
- A modular service-layer architecture (routers call services, services call external APIs) keeps LLM/TTS provider swaps and unit testing isolated from route handlers, per the resume's own "versioned API contracts" and "modular" claims.
- Keeping LLM/TTS calls provider-agnostic (env-driven base URL + key) matches the resume's generic phrasing and avoids committing to a vendor the user hasn't chosen yet.

### 6. Alternatives Considered

#### Alternative A

**Approach:**  
Keep the Node.js stack declared in the existing `CLAUDE.md` and build the backend in Express instead.

**Why rejected:**  
User explicitly chose Python/FastAPI when asked to resolve the conflict between the resume (Python) and the template boilerplate (Node.js).

#### Alternative B

**Approach:**  
Hardcode a specific LLM provider (OpenAI) and TTS provider (ElevenLabs) with their SDKs directly in the service layer.

**Why rejected:**  
User asked to "stick to the description" and, when asked directly which providers to integrate, said to use what's written in the resume — which only says "LLM API" / "TTS API" generically. Built a generic HTTP-based adapter instead so a concrete provider can be plugged in later via `.env` only.

### 7. Files Modified

| File | Change | Reason |
|---|---|---|
| `CLAUDE.md` | Rewrote from Node.js boilerplate to real Python/FastAPI stack + conventions | Match actual project, confirmed with user |
| `README.md` | Rewrote from garbled Node.js template to project description mirroring the resume bullet | Match actual project |
| `.gitignore` | Rewrote from garbled `node_modules/` entry to a Python `.gitignore` | Previous file was wrong-language boilerplate |
| `requirements.txt`, `requirements-dev.txt` | Added | Python dependencies for FastAPI, SQLAlchemy, Alembic, auth, tests |
| `.env.example` | Added | Documents required env vars (DB, JWT secret, LLM/TTS API base URL + key) |
| `app/**` (main, core, db, models, schemas, services, api) | Added | Full FastAPI application scaffold |
| `alembic.ini`, `alembic/env.py`, `alembic/script.py.mako`, `alembic/versions/0001_initial_schema.py` | Added | Initial DB schema migration for users/contents/generation_history/voice_preferences/audio_assets |
| `Dockerfile`, `docker-compose.yml` | Added | Local dev environment (API + Postgres) |
| `tests/conftest.py`, `tests/test_content.py` | Added | Auth, content CRUD, generation-history, and TTS-language-validation tests against an in-memory SQLite DB |
| `DECISION_LOG.md` | Added (copied from user's Desktop template) | Bring the governance file into the repo it governs |

### 8. Dependencies / Configuration

```text
Added:
- fastapi, uvicorn[standard]
- sqlalchemy, alembic, psycopg2-binary
- pydantic[email], pydantic-settings
- python-jose[cryptography], passlib[bcrypt], bcrypt==4.0.1 (pinned — passlib 1.7.4 is incompatible with bcrypt>=4.1)
- httpx, python-dotenv, python-multipart, email-validator
- pytest, pytest-asyncio, ruff (dev only)

Removed:
- (none — no prior Python dependencies existed)

Environment variables:
- DATABASE_URL
- SECRET_KEY, ACCESS_TOKEN_EXPIRE_MINUTES
- LLM_API_BASE_URL, LLM_API_KEY, LLM_MODEL
- TTS_API_BASE_URL, TTS_API_KEY

Configuration:
- CLAUDE.md stack declaration: Node.js → Python/FastAPI/PostgreSQL
```

### 9. Result

```text
Test:
Ran `pytest tests/ -v` (5 tests: register/login, content create+get,
LLM generate persisting to generation_history, TTS rejecting an
unsupported language code, TTS returning a stub audio URL when no
TTS_API_KEY is configured) against an in-memory SQLite DB.

Also ran `alembic upgrade head --sql` in offline mode to validate the
initial migration's generated SQL matches the SQLAlchemy models
(no live Postgres was available in this environment — Docker is not
installed, so the migration has NOT been run against real Postgres).

Expected:
All 5 tests pass; migration SQL is valid DDL for all 5 tables.

Actual:
All 5 tests passed after fixing two real bugs surfaced during testing
(see below). Migration SQL generated cleanly and matches the models.

Status:
PASS (against SQLite + offline migration check).
NOT YET VERIFIED against real Postgres or real LLM/TTS provider APIs —
those require Docker and real API keys, neither available here.
```

Two bugs were found and fixed while testing, not just written and assumed correct:
1. `passlib[bcrypt]` combined with `bcrypt==5.0.0` raised `ValueError: password cannot be longer than 72 bytes` on any login, because passlib 1.7.4 can't read `bcrypt.__about__` on bcrypt>=4.1 and mis-handles the secret. Fixed by pinning `bcrypt==4.0.1`.
2. `get_current_user` in `app/api/deps.py` passed the JWT `sub` claim (a string) straight into `db.get(User, user_id)`, which failed under SQLAlchemy's UUID type adapter (`AttributeError: 'str' object has no attribute 'hex'`). Fixed by parsing it into a `uuid.UUID` first, with a 401 on a malformed value.

### 10. Trade-offs / Risks

- LLM/TTS services are generic HTTP adapters, not official SDKs — once a real provider is chosen, its actual request/response shape will very likely differ from the placeholder `{"model", "prompt"} → {"output"}` / `{"text","language","voice_id"} → {"audio_url"}` contracts assumed here, and `llm_service.py`/`tts_service.py` will need a follow-up decision entry to match the real API.
- No live Postgres or Docker verification was possible in this environment — schema correctness is confirmed via offline SQL generation only, not an actual `alembic upgrade head` against a running database.
- Auth is minimal (email/password + JWT, no refresh tokens, no roles) — adequate for a portfolio project, not production-grade multi-tenant auth.

### 11. Rollback

```text
Revert:
- Delete app/, alembic/, tests/, Dockerfile, docker-compose.yml,
  requirements*.txt, .env.example
- Restore CLAUDE.md, README.md, .gitignore to their prior (template) content
- Revert commit: (see git log after this entry's commit)
```

### 12. AI Reasoning Summary

> The AI made this change because the user asked to build the resume-described backend now, and the repo only had unedited Node.js template boilerplate standing in for it.  
> The previous implementation had no real code, and its `CLAUDE.md`/`README.md` described a different stack than what was actually wanted.  
> The new implementation is a modular FastAPI service with a Postgres data layer, JWT auth, and provider-agnostic LLM/TTS service abstractions, backed by a passing test suite and a validated (offline) Alembic migration.  
> This was preferred over hardcoding a specific LLM/TTS vendor or keeping the Node.js stack because the user directly confirmed Python/FastAPI, and directly said to keep the LLM/TTS description as generic as the resume states it.
