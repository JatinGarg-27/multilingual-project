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

---

## DECISION-003 — Verify Alembic migration against real Postgres via docker compose

**Date:** 2026-08-18  
**Status:** Accepted  
**Type:** Testing

### 1. Trigger

DECISION-001 and DECISION-002 both explicitly flagged the same open risk: the schema had only been validated with `alembic upgrade head --sql` in offline mode (SQL generation only) and with SQLite in unit tests — never actually applied to a running Postgres instance, because the AI's sandbox has no Docker. User fixed their local Docker Desktop setup (virtualization was disabled, then WSL2 needed an update) and a typo'd `.env` file (`tts_service/.en` instead of `.env`), then ran the real stack.

### 2. Problem

Unknown whether `alembic/versions/0001_initial_schema.py` (hand-written, not autogenerated from a live DB, since no Postgres was ever available to autogenerate against) would actually apply cleanly to real Postgres — offline SQL generation checks syntax, not actual execution against a live server.

### 3. Previous Implementation

Schema validated only via:
- `alembic upgrade head --sql` (offline, no live DB)
- SQLAlchemy `Base.metadata.create_all()` against in-memory SQLite in pytest

Never run as `alembic upgrade head` against a real Postgres server.

### 4. Decision

No code change. User ran `docker compose up --build` (all 4 containers — `db`, `generation-service`, `tts-service`, `content-service` — came up and stayed running), then `docker compose exec content-service alembic upgrade head` against the live `db` Postgres 16 container.

### 5. Why This Decision?

This was the single largest unverified claim across DECISION-001 and DECISION-002's "Result"/"Trade-offs" sections. Per this file's own rule ("do not claim a fix works unless it was tested"), those entries correctly stated NOT YET VERIFIED rather than assuming success — this entry closes that out with an actual result instead of leaving it open indefinitely.

### 6. Alternatives Considered

Not applicable — this is a verification step, not a design choice between approaches.

### 7. Files Modified

None. Verification only; no code, schema, or config files changed.

### 8. Dependencies / Configuration

```text
Added: (none)
Removed: (none)
Environment variables: (none — user's local .env files already had the correct
  docker-compose-network values from the earlier setup steps)
Configuration: (none)
```

### 9. Result

```text
Test:
Ran `docker compose exec content-service alembic upgrade head`
against the live `db` (Postgres 16) container.

Expected:
Alembic reports "Running upgrade -> 0001, initial schema" with no
errors, and creates all 5 tables (users, contents, generation_history,
voice_preferences, audio_assets) plus its own alembic_version table.

Actual:
Output:
  INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
  INFO  [alembic.runtime.migration] Will assume transactional DDL.
  INFO  [alembic.runtime.migration] Running upgrade  -> 0001, initial schema
No errors, no traceback. Matches the offline SQL that was validated
in DECISION-001.

Status:
PASS. The migration is now confirmed against real Postgres, not just
offline SQL generation or SQLite.
```

### 10. Trade-offs / Risks

- Table creation was verified; full CRUD/generate/speech request flow through the live Docker stack (via `:8000/docs`) has not yet been explicitly re-confirmed by the user in this environment — the app logic itself was already verified end-to-end in DECISION-002's local 3-process smoke test, so this is low-risk, but it's the one remaining gap before calling the whole stack fully verified.
- LLM/TTS provider integration is still unverified against a real provider (no API keys chosen yet) — unchanged from DECISION-001/002.

### 11. Rollback

```text
Not applicable — no changes were made, only verification.
```

### 12. AI Reasoning Summary

> The AI logged this because the user reported a successful `alembic upgrade head` run against the real Postgres container spun up by `docker compose`.  
> The previous implementation had this marked as an explicit open risk in two prior decision entries, since no Docker was available to the AI itself.  
> The new state is that the schema is now confirmed to work against real Postgres, not just offline-generated SQL.  
> This was recorded as its own entry rather than silently editing DECISION-001/002's Result sections because this file's chronological, append-only convention means new evidence gets a new entry, not a rewrite of what was known at the time.

---

## DECISION-004 — Wire real LLM (OpenAI) and TTS (ElevenLabs) providers

**Date:** 2026-08-18  
**Status:** Accepted  
**Type:** Feature

### 1. Trigger

User asked to complete the real LLM/TTS integration (previously left as a provider-agnostic stub per DECISION-001, at the user's own instruction to "stick to the description" and not invent a vendor). Asked which providers to use; user chose OpenAI (LLM) and ElevenLabs (TTS) from the options presented.

### 2. Problem

`generation_service` and `tts_service` only ever returned stub text/audio — `_call_llm`/`_call_elevenlabs`-equivalent code called a generic `{base_url}` with a guessed request/response shape (`{"model","prompt"} -> {"output"}` and `{"text","language","voice_id"} -> {"audio_url"}`), which does not match any real provider's actual API contract. Bullet 2 of the resume ("Integrating an LLM API to draft and refine content, paired with a TTS API...") was architecturally true but not functionally true — no real AI-generated content or audio was ever produced.

### 3. Previous Implementation

```text
generation_service/app/main.py:
  _call_llm(prompt) -> httpx.post(LLM_API_BASE_URL, json={"model","prompt"}) -> response.json()["output"]

tts_service/app/main.py:
  synthesize() -> httpx.post(TTS_API_BASE_URL, json={"text","language","voice_id"}) -> response.json()["audio_url"]
```
Neither shape matches a real provider. No audio storage existed — the (fictional) contract assumed the provider returned a ready-made URL.

### 4. Decision

- `generation_service`: rewrote to call OpenAI's real Chat Completions API — `POST https://api.openai.com/v1/chat/completions`, `Authorization: Bearer {OPENAI_API_KEY}`, body `{"model": OPENAI_MODEL, "messages": [{"role": "user", "content": prompt}]}`, parses `response.json()["choices"][0]["message"]["content"]`. Config renamed `LLM_API_*` → `OPENAI_API_KEY`/`OPENAI_BASE_URL`/`OPENAI_MODEL` (default `gpt-4o-mini`).
- `tts_service`: rewrote to call ElevenLabs' real text-to-speech API — `POST https://api.elevenlabs.io/v1/text-to-speech/{voice_id}`, `xi-api-key: {ELEVENLABS_API_KEY}` header (not `Authorization: Bearer` — ElevenLabs uses its own header), body `{"text", "model_id": "eleven_multilingual_v2"}`. ElevenLabs returns raw MP3 bytes, not JSON/a URL, so the service now writes the bytes to `audio_output/{uuid}.mp3` and serves them back via a new `StaticFiles` mount at `/audio`, returning `{PUBLIC_BASE_URL}/audio/{uuid}.mp3` as `audio_url`. Config renamed `TTS_API_*` → `ELEVENLABS_API_KEY`/`ELEVENLABS_BASE_URL`/`ELEVENLABS_MODEL_ID`/`DEFAULT_VOICE_ID`/`PUBLIC_BASE_URL`.
- Both services now return `502` (not an unhandled exception → generic 500) when the provider errors or is unreachable, via explicit `httpx.HTTPStatusError`/`httpx.RequestError` handling.
- `docker-compose.yml`: added a named volume (`tts_audio`) mounted at `/app/audio_output` in `tts-service`, so generated audio survives container restarts.
- Both services' `.env.example` updated with real signup URLs and the actual env var names.
- **Known gap, not hidden:** ElevenLabs' `eleven_multilingual_v2` model does not officially list Telugu or Kannada as supported languages (Tamil is supported). The system still accepts and forwards `te`/`kn` requests (our own `supported_languages` list is unchanged, since the resume/architecture claims all three Indian languages), but output quality/accuracy for those two is not guaranteed by the provider. This is documented in `tts_service/app/config.py`, `.env.example`, `CLAUDE.md`, and `README.md`.

### 5. Why This Decision?

- User directly chose OpenAI and ElevenLabs when asked; no ambiguity to resolve.
- ElevenLabs was already the AI's own earlier recommendation specifically because it covers more of the six required languages than alternatives — but "more" turned out not to mean "all three" Indian languages, which only became clear while implementing the real request format. Silently ignoring that gap would violate this file's own rule against overclaiming; documenting it lets the user decide whether to accept it, add a second provider for `te`/`kn` later, or note it as a known limitation in interviews.
- Storing audio to local disk + serving via a static mount is the minimal real implementation of "audio_url" that doesn't require standing up S3/cloud storage for a portfolio project, while still being a genuine file a client can play, not a fake stub string.

### 6. Alternatives Considered

#### Alternative A

**Approach:**  
Keep the LLM/TTS layer fully generic/provider-agnostic indefinitely, never calling a real API.

**Why rejected:**  
User explicitly asked to complete the real integration now — the resume bullet claims working LLM+TTS integration, and a stub-only implementation can't back that claim in a live demo.

#### Alternative B

**Approach:**  
For TTS, reject `te`/`kn` outright with a 400 (matching what ElevenLabs actually supports) instead of accepting-but-not-guaranteeing them.

**Why rejected:**  
The resume and the project's own `supported_languages` config explicitly claim all three Indian languages. Silently narrowing that without telling the user would be a bigger integrity problem than documenting the gap. Left the decision of whether to actually drop `te`/`kn` support (or add a second TTS provider for them) to the user.

### 7. Files Modified

| File | Change | Reason |
|---|---|---|
| `services/generation_service/app/config.py` | `LLM_API_*` → `OPENAI_API_KEY`/`OPENAI_BASE_URL`/`OPENAI_MODEL` | Match real OpenAI env var naming |
| `services/generation_service/app/main.py` | Real OpenAI Chat Completions request/response handling, 502 on provider error | Was a fictional generic contract |
| `services/generation_service/.env.example` | Real key names + signup URL | Match new config |
| `services/generation_service/tests/test_generation.py` | Added 2 tests mocking `httpx.post` to verify request construction (URL, headers, body) and 502 handling | Prove the request-building logic is correct without a real key |
| `services/tts_service/app/config.py` | `TTS_API_*` → `ELEVENLABS_API_KEY`/`ELEVENLABS_BASE_URL`/`ELEVENLABS_MODEL_ID`/`DEFAULT_VOICE_ID`/`PUBLIC_BASE_URL`; added `unverified_languages` | Match real ElevenLabs env vars; flag the te/kn gap in code |
| `services/tts_service/app/main.py` | Real ElevenLabs call, writes returned bytes to `audio_output/`, `StaticFiles` mount at `/audio`, 502 on provider error | ElevenLabs returns raw audio bytes, not a JSON URL — previous contract was fictional |
| `services/tts_service/.env.example` | Real key names, signup URL, te/kn caveat | Match new config |
| `services/tts_service/tests/test_tts.py` | Added 2 tests mocking `httpx.post`, verifying request construction and that bytes get written+served correctly via the `/audio` mount | Prove the file-storage/serving logic is correct without a real key |
| `docker-compose.yml` | Added `tts_audio` named volume mounted at `/app/audio_output` in `tts-service` | Generated audio should survive container restarts |
| `.gitignore` (root) | Added `audio_output/` | Generated files shouldn't be committed |
| `CLAUDE.md`, `README.md` | Name the real providers, document the te/kn gap | Match actual implementation |

### 8. Dependencies / Configuration

```text
Added:
- (none — httpx was already a dependency of both services; StaticFiles
  ships with FastAPI/Starlette, no new package needed)

Removed:
- (none)

Environment variables:
- generation_service: removed LLM_API_BASE_URL/LLM_API_KEY/LLM_MODEL;
  added OPENAI_API_KEY, OPENAI_BASE_URL, OPENAI_MODEL
- tts_service: removed TTS_API_BASE_URL/TTS_API_KEY; added
  ELEVENLABS_API_KEY, ELEVENLABS_BASE_URL, ELEVENLABS_MODEL_ID,
  DEFAULT_VOICE_ID, PUBLIC_BASE_URL

Configuration:
- docker-compose.yml: added tts_audio named volume for tts-service
```

### 9. Result

```text
Test:
Ran the full suite for both changed services:
  services/generation_service: pytest tests/  -> 5 passed
  services/tts_service:        pytest tests/  -> 8 passed
  services/content_service:    pytest tests/  -> 5 passed (unaffected,
    re-ran to confirm — content_service's HTTP clients talk to the
    same response shape both services still return, unchanged)
New tests mock httpx.post/response to verify: the exact URL, headers,
and JSON body sent to the real provider endpoints; correct parsing of
the response; that a provider error/timeout surfaces as 502 not a
raw exception; and (TTS) that returned bytes are actually written to
disk and served back byte-for-byte through the /audio static mount.

Expected:
All tests pass; request construction matches each provider's
documented API contract.

Actual:
All 18 tests passed (5+8+5).

Status:
PASS for request-construction/response-parsing logic and the file
storage/serving mechanism — all verified by mocking httpx, since no
real OPENAI_API_KEY or ELEVENLABS_API_KEY is available in this
environment.
NOT YET VERIFIED: an actual live call to OpenAI's or ElevenLabs' real
API. The AI has no internet-reachable credentials for either provider.
This can only be confirmed once the user adds a real key to
services/generation_service/.env and services/tts_service/.env and
tries it (e.g. through the docker compose stack already running).
```

### 10. Trade-offs / Risks

- **Unverified against the live APIs** — API contracts, model names (`gpt-4o-mini`, `eleven_multilingual_v2`), and auth header conventions were implemented per documented/known-stable patterns, not confirmed against a real response. If either provider has changed something since, the first real call may need a small fix.
- **Telugu/Kannada gap** — see above. The resume's claim of covering all three Indian languages is not fully backed by the chosen TTS provider.
- **Audio storage is local-disk, ephemeral-by-default** — mitigated with a docker volume, but this is not a production-grade asset store (no CDN, no cleanup/retention policy, single-container storage doesn't scale horizontally). Fine for a portfolio project; would need S3/GCS + a CDN for real scale.
- **`gpt-4o-mini` / `eleven_multilingual_v2` are point-in-time model names** — both providers periodically deprecate/rename models; `OPENAI_MODEL`/`ELEVENLABS_MODEL_ID` are configurable via env so this doesn't require a code change if a model is retired.

### 11. Rollback

```text
Revert:
- Restore services/generation_service/app/{main,config}.py and
  services/tts_service/app/{main,config}.py from the DECISION-003
  commit (back to generic-provider stub behavior)
- Restore the corresponding .env.example files
- Remove the StaticFiles mount / audio_output storage from tts_service
- Remove the tts_audio volume from docker-compose.yml
- Revert commit: (see git log after this entry's commit)
```

### 12. AI Reasoning Summary

> The AI made this change because the user asked to complete the real LLM/TTS integration and chose OpenAI and ElevenLabs when given the choice.  
> The previous implementation called a fictional generic API contract that no real provider actually implements, so nothing real was ever generated.  
> The new implementation calls each provider's actual documented API, handles their real response shapes (including ElevenLabs returning raw audio bytes instead of a URL, which required adding local file storage + static serving), and fails cleanly (502) instead of crashing when a provider errors.  
> This was preferred over staying generic (doesn't satisfy the user's explicit request) or silently picking different providers (the user was asked and chose these two) — and the discovered Telugu/Kannada coverage gap was documented rather than hidden, per this file's own honesty rules, since it directly affects whether the resume's claim is fully accurate.
