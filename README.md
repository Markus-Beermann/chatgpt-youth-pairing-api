# ChatGPT Youth – Pairing API Skeleton

This is a **minimal FastAPI skeleton** for the Child ↔ Parent pairing flow.

## Features (v0)
- Roles: `child`, `parent` (JWT stubbed).
- Create pairing code (parent).
- Claim pairing code (child).
- Hash-only storage for codes (Argon2id + server-side pepper).
- Simple TTL checks, mark-as-used, in-memory rate-limit demo.
- Structured JSON logging with PII-free audit events.

> **Note:** Persistence is in-memory for v0 to keep it simple. Next step is SQLite/PostgreSQL and Redis for rate limiting.

---

## Quickstart

```bash
# 1) Create and activate a virtualenv
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 2) Install deps
pip install -r requirements.txt

# 3) Copy env example and set a strong PEPPER
cp .env.example .env
# edit .env and change PAIR_PEPPER="super-long-random-string"

# 4) Run dev server
uvicorn app.main:app --reload
```

Open: http://127.0.0.1:8000/docs

---

## Endpoints (v1)

- `POST /v1/pairing/create` (Parent JWT) → Creates a code with TTL
- `POST /v1/pairing/claim` (Child JWT)   → Claims a code and creates a pairing
- `GET  /v1/pairings` (Any JWT)          → Lists pairings for the actor
- `DELETE /v1/pairings/{id}`           → Revokes a pairing

Auth is stubbed with a dependency that injects a demo user by role via headers.

### Demo Headers
- For **parent**: `x-demo-role: parent`, `x-demo-user: u_parent_1`
- For **child**:  `x-demo-role: child`,  `x-demo-user: u_child_1`

---

## cURL Demo

```bash
# Create a pairing code (Parent)
curl -s -X POST http://127.0.0.1:8000/v1/pairing/create   -H 'x-demo-role: parent' -H 'x-demo-user: u_parent_1' | jq .

# Claim the code (Child) – replace ABC-123 with the code you got
curl -s -X POST http://127.0.0.1:8000/v1/pairing/claim   -H 'Content-Type: application/json'   -H 'x-demo-role: child' -H 'x-demo-user: u_child_1'   -d '{"code":"ABC-123"}' | jq .

# List pairings (either role)
curl -s http://127.0.0.1:8000/v1/pairings -H 'x-demo-role: child' -H 'x-demo-user: u_child_1' | jq .
```

---

## Project Structure

```
app/
  __init__.py
  main.py
  config.py
  logging.py
  deps.py
  db.py
  models.py
  security/
    hashing.py
    rate_limit.py
  routers/
    auth.py
    pairing.py
.env.example
requirements.txt
.gitignore
README.md
```

---

## Next Steps
- Replace in-memory stores with DB (SQLite/PostgreSQL) and Redis for rate limiting.
- Implement real JWT auth (PyJWT) and device binding.
- Add WebSocket for real-time events.
- Extend audit logs with hash-chaining, WORM storage, and retention.
