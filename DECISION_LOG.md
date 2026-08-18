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

---

## DECISION-002 — Split monolith into content/generation/tts microservices

**Date:** 2026-08-18  
**Status:** Accepted  
**Type:** Architecture

### 1. Trigger

User shared the full resume bullet text, which included a 4th bullet not previously visible: *"Structuring the service with a modular, microservice-oriented architecture so generation, TTS conversion, and persistence layers can scale and be tested independently."* User then directly asked whether the implementation so far matched the description, and asked the AI to complete as much as possible on its own.

### 2. Problem

DECISION-001's implementation was a single FastAPI process (`app/`) where `llm_service.py` and `tts_service.py` were plain Python modules called in-process by route handlers. That satisfies bullets 1–3 (REST CRUD, LLM+TTS integration, versioned Postgres data layer) but does not satisfy bullet 4: generation, TTS conversion, and persistence were not independently deployable, scalable, or testable — they were one process, one test suite, one deploy unit.

### 3. Previous Implementation

```text
multilingual-project/
├── app/
│   ├── api/v1/routers/{content,generation,speech,voices,auth}.py
│   ├── services/{llm_service.py, tts_service.py, content_service.py}
│   ├── models/, schemas/, db/, core/
│   └── main.py
├── alembic/
├── tests/
├── Dockerfile
└── requirements.txt
```
One FastAPI app; `generation.py`/`speech.py` routers imported `llm_service`/`tts_service` directly and called their methods in-process.

### 4. Decision

Split the single app into three independently deployable services under `services/`:

- `content_service/` — the former `app/`, minus the LLM/TTS modules. Owns Postgres (all 5 tables), auth, and the public `/api/v1` REST API. Calls the other two services over HTTP via new `app/services/generation_client.py` and `app/services/tts_client.py` (replacing the old `llm_service.py`/`tts_service.py`).
- `generation_service/` — new standalone FastAPI app (`POST /generate`, `POST /refine`). Stateless, no DB, no auth — just wraps the LLM API call.
- `tts_service/` — new standalone FastAPI app (`POST /synthesize`, `GET /languages`, `GET /voices/{language}`). Stateless, no DB.

Each service has its own `requirements.txt`, `Dockerfile`, `.env.example`, and `tests/`. `docker-compose.yml` at the repo root now runs `db` + all three services, each on its own port (8000/8001/8002). `content_service`'s config gained `GENERATION_SERVICE_URL`/`TTS_SERVICE_URL` and lost `LLM_API_*`/`TTS_API_*` (those moved to the respective sub-service's own config).

### 5. Why This Decision?

- The resume bullet explicitly claims generation, TTS, and persistence "can scale and be tested independently" — an in-process monolith cannot honestly claim that; three separately deployable HTTP services can (each has its own container, its own test suite that runs without the others, and can be scaled/replicated on its own).
- `llm_service`/`tts_service` already had narrow, single-purpose interfaces from DECISION-001, which made the extraction mechanical: turn the class methods into route handlers, turn the caller into an HTTP client with the same method signatures.

### 6. Alternatives Considered

#### Alternative A

**Approach:**  
Keep the modular monolith and describe "microservice-oriented" as referring only to the internal service-layer separation (routers → services), not literal separate deployables.

**Why rejected:**  
The bullet's own wording — "scale and be tested independently" — only becomes literally true with separate deployable units. A monolith can't be scaled or tested independently per-layer; scaling the process scales everything, and the test suite for LLM logic can't run without the whole app importing successfully.

#### Alternative B

**Approach:**  
Full microservices with each service owning its own database/message queue, and async messaging (e.g. a queue) between them instead of synchronous HTTP.

**Why rejected:**  
Over-engineered for this project's actual scope. `generation_service` and `tts_service` are stateless API wrappers with no data to own — giving them their own databases would create data ownership questions with no benefit. Synchronous HTTP (`httpx`) is simpler to run, test, and reason about than introducing a message broker, and still satisfies "scale and be tested independently."

### 7. Files Modified

| File | Change | Reason |
|---|---|---|
| `app/**` → `services/content_service/app/**` | Moved (git mv) | Content service now lives under `services/` alongside its peers |
| `alembic/`, `alembic.ini`, `tests/`, `Dockerfile`, `requirements*.txt`, `.env.example` → `services/content_service/...` | Moved (git mv) | Same |
| `services/content_service/app/services/llm_service.py` → `generation_client.py` | Rewrote | Now an HTTP client calling generation-service instead of calling the LLM API directly |
| `services/content_service/app/services/tts_service.py` → `tts_client.py` | Rewrote | Now an HTTP client calling tts-service instead of calling the TTS API directly |
| `services/content_service/app/api/v1/routers/generation.py`, `speech.py` | Updated imports/calls | Use the new HTTP clients; `generation.py` now reads `model`/`output` from the client's JSON response |
| `services/content_service/app/core/config.py` | Replaced `llm_api_*`/`tts_api_*` with `generation_service_url`/`tts_service_url` | Those settings moved to the sub-services that own them |
| `services/content_service/app/main.py` | Updated `UnsupportedLanguageError` import to `tts_client` | Module moved |
| `services/content_service/tests/conftest.py` | Added `fake_peer_services` autouse fixture | Unit tests must not require the other two services to be running |
| `services/generation_service/**` (new) | Added | Standalone LLM microservice: `app/main.py`, `app/config.py`, `requirements.txt`, `Dockerfile`, `.env.example`, `tests/test_generation.py` |
| `services/tts_service/**` (new) | Added | Standalone TTS microservice: same shape as above, `tests/test_tts.py` |
| `docker-compose.yml` (root) | Rewrote | Orchestrates `db` + `generation-service` + `tts-service` + `content-service` |
| `CLAUDE.md`, `README.md` (root) | Rewrote | Describe the 3-service architecture instead of the single-app one |

### 8. Dependencies / Configuration

```text
Added:
- generation_service and tts_service each get their own minimal
  requirements.txt (fastapi, uvicorn, pydantic, pydantic-settings,
  httpx, python-dotenv) — no SQLAlchemy/Alembic/passlib, since they
  own no data and no auth.

Removed:
- (none — content_service keeps its full dependency set)

Environment variables:
- content_service: removed LLM_API_BASE_URL/LLM_API_KEY/LLM_MODEL/
  TTS_API_BASE_URL/TTS_API_KEY; added GENERATION_SERVICE_URL,
  TTS_SERVICE_URL
- generation_service (new .env): LLM_API_BASE_URL, LLM_API_KEY, LLM_MODEL
- tts_service (new .env): TTS_API_BASE_URL, TTS_API_KEY

Configuration:
- docker-compose.yml: single `api` service → `generation-service` (8001)
  + `tts-service` (8002) + `content-service` (8000), each built from
  its own directory under services/
```

### 9. Result

```text
Test:
Ran the full test suite for all three services separately:
  services/content_service:    pytest tests/  -> 5 passed
  services/generation_service: pytest tests/  -> 3 passed
  services/tts_service:        pytest tests/  -> 6 passed
(content_service's tests mock the two HTTP peers via an autouse
monkeypatch fixture, so they don't require generation-service/
tts-service to be running.)

Also ran a live end-to-end smoke test: started all three services as
real separate uvicorn processes (content-service pointed at a
throwaway SQLite DB, since no Postgres/Docker is available in this
environment) and drove a full HTTP flow — register, login, create
content, POST /generate (round-tripped through generation-service on
:8001), POST /speech (round-tripped through tts-service on :8002).

Expected:
All three test suites pass in isolation; the live flow produces a
generated draft and a stub audio_url via real inter-process HTTP
calls, not mocks.

Actual:
All 14 tests passed. The live smoke test succeeded exactly as
expected — /generate returned the generation-service's stub output,
/speech returned the tts-service's stub audio_url — confirming the
three processes are genuinely decoupled and talking over HTTP.

Status:
PASS. Still NOT verified against real Postgres (no Docker here) or
against a real LLM/TTS provider (no API keys) — same caveat as
DECISION-001, now applying to two more services instead of one.
```

### 10. Trade-offs / Risks

- More moving parts: three services to run instead of one, three `.env` files, inter-service network calls that can fail (timeouts, connection errors) in ways an in-process call cannot — none of that error handling has been hardened yet (a down generation-service currently surfaces as an unhandled `httpx` exception → 500, not a clean error).
- Local dev now requires either `docker compose up` or manually running three separate `uvicorn` processes, instead of one.
- Slightly higher latency per request (two network hops for a full generate+speech flow instead of in-process calls) — irrelevant at portfolio scale, would matter at real production scale.
- Easier to honestly demonstrate/explain "microservice-oriented, independently scalable and testable" in an interview, since it's now literally true rather than an internal implementation detail.

### 11. Rollback

```text
Revert:
- git mv services/content_service/{app,alembic,alembic.ini,tests,Dockerfile,requirements*.txt,.env.example} back to repo root
- Restore app/services/llm_service.py and tts_service.py from the DECISION-001 commit
- Delete services/generation_service/ and services/tts_service/
- Restore the single-service docker-compose.yml, CLAUDE.md, README.md from the DECISION-001 commit
- Revert commit: (see git log after this entry's commit)
```

### 12. AI Reasoning Summary

> The AI made this change because the user surfaced the resume's 4th bullet ("microservice-oriented architecture... scale and be tested independently") and directly asked whether the build matched it — it did not.  
> The previous implementation was a modular monolith: clean internal service boundaries, but one deployable process, so nothing could actually scale or be tested independently of anything else.  
> The new implementation is three separately deployable FastAPI services (content persistence+API, LLM generation, TTS conversion) communicating over HTTP, each with its own tests, Dockerfile, and dependencies.  
> This was preferred over keeping the monolith (doesn't match the explicit claim) or going further into full data-owning microservices with async messaging (unnecessary complexity for two stateless API-wrapper services) because it's the minimal change that makes the resume's specific wording literally true, verified with a live 3-process HTTP smoke test.
