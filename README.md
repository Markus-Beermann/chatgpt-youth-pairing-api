ChatGPT Youth – Pairing API

A FastAPI-based parent/child pairing API, serving as the backend foundation for the ChatGPT Youth App.
This project started as a minimal skeleton and is evolving step by step into a fully functional backend service.

✨ Features (as of October 2025)

✅ Create pairing code (POST /v1/pairing/create)

✅ Claim pairing code (POST /v1/pairing/claim)

✅ List pairings (GET /v1/pairing)

📝 Tests with pytest and httpx

🔜 Revoke pairing (DELETE /v1/pairing/{id}) – planned

🔜 CI/CD Workflow with GitHub Actions – planned

Note: Persistence is currently in-memory to keep it simple.
Next step: add SQLite/PostgreSQL and Redis for rate limiting.

⚙️ Installation & Start
# 1) Create and activate a virtualenv
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 2) Install dependencies
pip install -r requirements.txt -r requirements-dev.txt

# 3) Copy env example and set a strong pepper
cp .env.example .env
# edit .env and change PAIR_PEPPER="super-long-random-string"

# 4) Run the dev server
uvicorn app.main:app --reload


The API will be available at:
👉 http://127.0.0.1:8000

👉 Swagger UI: http://127.0.0.1:8000/docs

📡 API Endpoints (v1)

POST /v1/pairing/create (Parent) → Creates a code with TTL

POST /v1/pairing/claim (Child) → Claims a code and creates a pairing

GET /v1/pairing (Any role) → Lists pairings for the actor

DELETE /v1/pairing/{id} (Parent) → Revokes a pairing (planned)

🔐 Demo Authentication

Auth is stubbed with headers for now:

Parent

x-demo-role: parent
x-demo-user: u_parent_1


Child

x-demo-role: child
x-demo-user: u_child_1

🖥️ cURL Examples
# Create a pairing code (Parent)
curl -s -X POST http://127.0.0.1:8000/v1/pairing/create \
  -H 'x-demo-role: parent' -H 'x-demo-user: u_parent_1' | jq .

# Claim the code (Child) – replace ABC-123 with the code you got
curl -s -X POST http://127.0.0.1:8000/v1/pairing/claim \
  -H 'Content-Type: application/json' \
  -H 'x-demo-role: child' -H 'x-demo-user: u_child_1' \
  -d '{"code":"ABC-123"}' | jq .

# List pairings (Child)
curl -s http://127.0.0.1:8000/v1/pairing \
  -H 'x-demo-role: child' -H 'x-demo-user: u_child_1' | jq .

📂 Project Structure
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
requests/
  pairing.http
tests/
  test_pairing.py
.env.example
requirements.txt
requirements-dev.txt
README.md

🧪 Tests

Run automated tests with:

pytest -v


Tests use FastAPI’s TestClient and do not require a running server.

🛣 Roadmap (Project Plan)

Goal: Backend completed by end of November 2025.

Phase 1 – Backend Core (October 2025)

Finalize REST API endpoints

Define & migrate database schema (SQLite → PostgreSQL-ready)

Add basic unit tests for API + DB

Phase 2 – Security & Authentication (November 2025)

Implement JWT-based authentication

Role model (Parent/Youth)

Logging + rate-limit checks (Redis planned)

Phase 3 – GPT Integration (Late November 2025)

Connect GPT API with pre-prompts

Test safety layer and edge cases

Log GPT interactions for audit

Phase 4 – Frontend / App (December 2025 – January 2026)

React Native proof of concept

Connect to backend API

Youth branding and UI testing

Phase 5 – Testing & Demo (January 2026)

CI/CD pipeline with GitHub Actions

Automated test coverage

Demo + documentation for tutor presentation

🚀 Next Steps

Replace in-memory store with SQLite/PostgreSQL

Add Redis for rate limiting

Implement real JWT auth (PyJWT) and device binding

Add WebSockets for real-time events

Extend audit logs with hash-chaining and retention policies