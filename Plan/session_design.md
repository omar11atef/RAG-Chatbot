# 🗂️ Session-Based Chat — Backend Design
> .NET 9 · Clean Architecture · Result Pattern

---

## 🧠 Core Idea

Every conversation lives inside a **Session**. A session has:
- A unique ID
- An owner (optional: by IP or user token)
- A **message limit** (e.g. max 10 questions)
- A **message counter**
- A full **history** of Q&A pairs in order

When the frontend sends a question, it includes the `sessionId`. The backend loads the history of that session, appends it to the RAG request as context, and enforces the message limit.

---

## 🗃️ Database Changes

### New Table: `Sessions`

| Column | Type | Description |
|---|---|---|
| `Id` | `GUID` (PK) | Unique session identifier, generated on creation |
| `CreatedAt` | `DateTime` | When the session started |
| `ExpiresAt` | `DateTime` | Optional: auto-expire after e.g. 2 hours of inactivity |
| `MessageCount` | `int` | How many questions have been asked so far |
| `MessageLimit` | `int` | Max allowed questions (default: 10) |
| `IsActive` | `bool` | False once limit is reached or session is closed |

---

### Updated Table: `ConversationLogs`

Add two new columns to the existing table:

| Column | Type | Description |
|---|---|---|
| `SessionId` | `GUID` (FK → Sessions) | Links each message to its session |
| `TurnIndex` | `int` | The order of this Q&A within the session (1, 2, 3...) |

This allows the backend to reconstruct the full ordered history of any session by querying `WHERE SessionId = ? ORDER BY TurnIndex ASC`.

---

## 🔌 New / Updated Endpoints

---

### 1. `POST /api/session`
**Type:** Command Endpoint
**Description:** Creates a new session and returns its ID. The frontend must call this before starting a conversation. The session ID is then stored client-side (localStorage or state) and sent with every subsequent chat request.

**How to handle it:**
- Generate a new `GUID` as the session ID
- Insert a new row in `Sessions` with `MessageCount = 0`, `MessageLimit = 10`, `IsActive = true`
- Return the session ID to the frontend
- No authentication required for a small project — session ID itself acts as the key

---

### 2. `POST /api/chat` *(Updated)*
**Type:** Command Endpoint (existing, extended)
**Description:** Now requires a `sessionId` in the request body alongside the question. Before forwarding to the Python RAG service, the backend validates the session and enriches the RAG request with conversation history.

**How to handle it (step by step):**

1. **Receive** `{ sessionId, question }`
2. **Validate session exists** → if not found, return `404 Session not found`
3. **Check `IsActive`** → if `false`, return `429 Session limit reached` (this is the "11th message" response)
4. **Check `MessageCount < MessageLimit`** → extra guard
5. **Load history** → query `ConversationLogs WHERE SessionId = ? ORDER BY TurnIndex ASC` → build an ordered list of `{ turn, question, answer }` pairs
6. **Build RAG request** → send to Python `/query` as `{ question, history: [...] }` — the Python service uses this history as conversation context for the LLM
7. **Receive answer** from Python
8. **Save to DB** → insert a new `ConversationLog` row with `SessionId`, `TurnIndex = MessageCount + 1`
9. **Increment `MessageCount`** on the session row
10. **If `MessageCount` now equals `MessageLimit`** → set `IsActive = false`
11. **Return** `{ answer, sources, turnIndex, remainingMessages }`

---

### 3. `GET /api/session/{sessionId}`
**Type:** Query Endpoint
**Description:** Returns the current state of a session — how many messages have been used, how many remain, and the full conversation history. Useful for the frontend to restore a chat on page reload.

**How to handle it:**
- Look up the session by ID
- Load all `ConversationLogs` for that session ordered by `TurnIndex`
- Return `{ sessionId, messageCount, messageLimit, remainingMessages, isActive, history: [...] }`

---

### 4. `DELETE /api/session/{sessionId}`
**Type:** Command Endpoint
**Description:** Closes a session manually before the limit is reached. The user can "start fresh" by ending the current session and creating a new one.

**How to handle it:**
- Find the session
- Set `IsActive = false`
- Return `204 No Content`

---

## ⚙️ New Services

---

### `SessionService`
**Type:** Application Service
**Description:** Owns all session lifecycle logic — creation, validation, limit enforcement, and closure. All session-related operations in `ChatController` and `SessionController` go through this service.

**Responsibilities:**
- Create a new session
- Validate a session ID (exists + active)
- Check and enforce the message limit
- Mark a session as inactive when the limit is hit or on manual close
- Return the remaining message count

---

### `ConversationContextBuilder`
**Type:** Domain / Application Service
**Description:** Given a `sessionId`, loads the ordered Q&A history and formats it into the structure the Python RAG service expects. This is the piece that gives the LLM "memory" within a session.

**Responsibilities:**
- Query `ConversationLogs` by session ID, ordered by `TurnIndex`
- Build the history array: `[{ turn: 1, q: "...", a: "..." }, ...]`
- Trim history if it gets too long (e.g. only send last 6 turns to avoid token overflow)
- Return the formatted context to be injected into the RAG request

---

### Updated `ChatService`
**Type:** Application Service (existing, extended)
**Description:** Now orchestrates session validation, context building, RAG call, and session state update in a single flow.

**New responsibilities added:**
- Call `SessionService.ValidateAsync(sessionId)` before proceeding
- Call `ConversationContextBuilder.BuildAsync(sessionId)` to get history
- Pass history to `RagHttpClient` alongside the question
- After receiving the answer, call `SessionService.RecordTurnAsync(sessionId, question, answer)`

---

## 📤 Updated Request / Response Contracts

### `POST /api/chat` — Updated Request Body
| Field | Type | Required | Description |
|---|---|---|---|
| `sessionId` | `GUID` | ✅ Yes | The active session this question belongs to |
| `question` | `string` | ✅ Yes | The student's question |

### `POST /api/chat` — Updated Success Response (200)
| Field | Type | Description |
|---|---|---|
| `answer` | `string` | LLM-generated answer |
| `sources` | `SourceResponse[]` | Retrieved document citations |
| `turnIndex` | `int` | Which turn this was (e.g. 7 of 10) |
| `remainingMessages` | `int` | How many questions the user has left |

### New Error Response: `429 – Limit Reached`
```
{
  "status": 429,
  "title": "Session limit reached",
  "errors": ["This session has reached its 10-message limit. Please start a new session."]
}
```

---

## 🔗 What Needs to Change in the Python RAG Service

The Python `/query` endpoint must accept the new `history` field:

| Field | Type | Description |
|---|---|---|
| `question` | `string` | Current question (unchanged) |
| `history` | `array` | List of previous `{ q, a }` pairs from this session |

The Python side injects this history into the LLM system prompt as prior conversation context, so the model can reference "question 4's answer" when answering "question 6". This is the only change required from the AI/Model person.

---

## 🔁 Full Request Flow (Updated)

```
Frontend
  → POST /api/chat { sessionId, question }
      → SessionService: validate session + check limit
      → ConversationContextBuilder: load history from DB
      → RagHttpClient: POST /query { question, history }
          → Python RAG: retrieves docs + uses history as LLM context
          → Returns { answer, sources }
      → ChatService: save turn to ConversationLogs
      → SessionService: increment MessageCount, deactivate if limit hit
  → Response: { answer, sources, turnIndex, remainingMessages }
```
