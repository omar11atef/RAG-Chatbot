# Backend Guide - University RAG Chatbot (Updated)

## 1. ✅ Project Summary
- Main idea: build a session-based university chatbot where each chat belongs to a session, history is reused for context, and answers come from a RAG service with citations.
- Current flow: Frontend -> FastAPI Backend -> RAG Service (`/query`) -> Backend response to frontend.
- What already exists in this repo:
  - API app bootstrap and global error handler (`main.py`)
  - Chat and trigger routers (`api/routers.py`)
  - Result/Error pattern (`domain/abstractions.py`, `domain/errors.py`)
  - Request/response contracts with validation (`application/contracts.py`)
  - Application services skeleton (`application/services.py`)
- Current limitation: the RAG client is mocked, and session-aware conversation is not implemented yet.

## 2. 🧩 Missing Parts
- Real HTTP integration:
  - `RagServiceClient` in `api/dependencies.py` still returns simulated data.
- Session lifecycle and memory:
  - Missing `POST /api/session`, `GET /api/session/{id}`, `DELETE /api/session/{id}`.
  - Missing session limit enforcement (for example 10 messages/session).
  - Missing history retrieval and turn indexing for contextual RAG calls.
- Persistence:
  - No database, repositories, or migrations yet (`ConversationLogs`, `Sessions` not implemented).
- Reliability and security:
  - No timeout/retry/circuit-breaker policy around outbound RAG calls.
  - No API key/JWT enforcement in routers.
  - No webhook signature validation or idempotency key handling for triggers.
- Operations:
  - `requirements.txt` is empty.
  - No tests (unit/integration) for chat/session critical paths.

## 3. 🛠️ Improved Architecture
- Keep clean layering already started in code:
  - `domain`: Result/Error/value rules, session constraints, invariants.
  - `application`: use-case services (`ChatService`, `SessionService`, `TriggerService`).
  - `infrastructure`: HTTP clients, repositories, DB models/migrations.
  - `api`: routers, dependency wiring, auth, request/response mapping.
- Proposed request orchestration for chat:
  1. Validate input + auth.
  2. Validate session exists and active.
  3. Load ordered history for session (possibly last N turns).
  4. Call RAG service with `{ question, history }`.
  5. Persist turn and increment message count atomically.
  6. Return answer + sources + turnIndex + remainingMessages.
- Use one transaction for "save turn + increment counter" to avoid race conditions with concurrent requests.

## 4. 🔗 API Design
- `POST /api/session`
  - Request: optional `messageLimit`.
  - Response: `{ sessionId, messageLimit, messageCount, isActive, expiresAt }`.
- `GET /api/session/{sessionId}`
  - Response: session state + ordered history.
- `DELETE /api/session/{sessionId}`
  - Behavior: close/deactivate session.
- `POST /api/chat`
  - Request:
    ```json
    { "sessionId": "guid", "question": "How to apply for CS?" }
    ```
  - Response:
    ```json
    {
      "answer": "....",
      "sources": [{ "file_name": "admissions.pdf", "page": 3, "snippet": "..." }],
      "turnIndex": 4,
      "remainingMessages": 6
    }
    ```
  - Errors:
    - `400` invalid payload/question
    - `404` session not found
    - `429` session limit reached
    - `503` RAG unavailable
- `POST /api/trigger`
  - Request includes signed webhook metadata + idempotency key.
  - Response: accepted/ignored/failed with reason.

## 5. ⚙️ Backend Enhancements
- Replace mock RAG calls with `httpx.AsyncClient`:
  - configure connect/read timeouts
  - retry transient failures with capped backoff
  - map transport failures to `Result.failure(ChatErrors.RagServiceUnavailable)`
- Add persistence:
  - Use SQLAlchemy + Alembic (or PostgreSQL first, SQLite acceptable for local demo).
  - Tables:
    - `sessions(id, created_at, expires_at, message_count, message_limit, is_active, last_activity_at)`
    - `conversation_logs(id, session_id, turn_index, question, answer, created_at)`
  - Add unique constraint `(session_id, turn_index)`.
- Add API security baseline:
  - Validate backend API key/JWT for frontend calls.
  - Validate HMAC signature for trigger/webhook endpoint.
  - Rate-limit chat endpoint by IP/session.
- Improve observability:
  - Add request correlation ID in middleware.
  - Structured logs (json) for chat latency, RAG latency, error codes, and sessionId.
- Improve configuration:
  - Move secrets to `.env`, never hardcode.
  - Add startup config validation (fail fast if required env vars missing).

## 6. 🎨 UX/UI Improvements
- Guided start cards:
  - "Admissions", "Faculties", "Scholarships", "Tuition", "Campus Life".
- Dynamic suggestions after each answer:
  - Example: "Ask about required documents", "Show deadline details".
- Smart clarification when intent is ambiguous:
  - "Did you mean undergraduate admissions or graduate admissions?"
- Interactive response blocks:
  - Source cards with file name + page + snippet.
  - "Open related topic" buttons that prefill follow-up questions.
- Session awareness on UI:
  - Show "Question 4 of 10" and remaining messages.
  - Show "Start new session" when limit is reached.

## 7. 📁 Folder Structure
```text
.
|-- api/
|   |-- routers/
|   |   |-- chat.py
|   |   |-- session.py
|   |   `-- trigger.py
|   |-- dependencies.py
|   `-- middleware.py
|-- application/
|   |-- contracts.py
|   |-- services/
|   |   |-- chat_service.py
|   |   |-- session_service.py
|   |   `-- trigger_service.py
|   `-- interfaces.py
|-- domain/
|   |-- abstractions.py
|   |-- errors.py
|   `-- entities.py
|-- infrastructure/
|   |-- http/
|   |   `-- rag_service_client.py
|   |-- persistence/
|   |   |-- models.py
|   |   |-- repositories.py
|   |   `-- db.py
|   `-- security/
|       `-- webhook_signature.py
|-- tests/
|   |-- unit/
|   `-- integration/
|-- core/
|   `-- config.py
`-- main.py
```

## 8. 🚀 Additional Suggestions
- Safe testing strategy for critical flows:
  1. Unit tests for session limit enforcement and Result mappings.
  2. Integration tests with mocked RAG timeout/503 responses.
  3. Concurrency test: two parallel chat calls on same session at limit boundary.
  4. Webhook idempotency test: same event replay should not double-process.
- Deployment readiness:
  - Add `/health` and `/ready` endpoints.
  - Add Dockerfile + compose for local full-stack run (frontend + backend + RAG + DB).
  - Add CI pipeline with lint, tests, and migration checks.
- Product improvements:
  - Cache common FAQ answers with TTL to reduce RAG latency/cost.
  - Add feedback endpoint (`thumbs_up/down`) to evaluate answer quality over time.
