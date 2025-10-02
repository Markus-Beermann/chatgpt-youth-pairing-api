# tests/conftest.py
import sys, os, pytest, uuid
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture(scope="session")
def client():
    return TestClient(app)


def _get_token(client: TestClient, email: str, password: str, role: str) -> str:
    signup = client.post("/v1/auth/signup", json={"email": email, "password": password, "role": role})
    if signup.status_code == 200:
        return signup.json()["access_token"]
    if signup.status_code == 409:  # already exists → login
        login = client.post("/v1/auth/login", json={"email": email, "password": password})
        assert login.status_code == 200, f"Login failed: {login.status_code} {login.text}"
        return login.json()["access_token"]
    raise AssertionError(f"Signup failed: {signup.status_code} {signup.text}")


def _new_email(prefix: str) -> str:
    return f"{prefix}+{uuid.uuid4().hex[:8]}@example.com"


@pytest.fixture
def parent_auth(client):
    email = _new_email("parent")
    token = _get_token(client, email, "secret123", "parent")
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def child_auth(client):
    email = _new_email("child")
    token = _get_token(client, email, "secret123", "child")
    return {"Authorization": f"Bearer {token}"}
