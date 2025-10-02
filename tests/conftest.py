import sys, os, pytest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture(scope="session")
def client():
    return TestClient(app)

def _signup(client: TestClient, email: str, password: str, role: str) -> str:
    r = client.post("/v1/auth/signup", json={"email": email, "password": password, "role": role})
    assert r.status_code in (200, 409)  # 409 if re-run; then login
    if r.status_code == 409:
        r = client.post("/v1/auth/login", json={"email": email, "password": password})
        assert r.status_code == 200
    token = r.json()["access_token"] if "access_token" in r.json() else r.json().get("access_token")
    return token

@pytest.fixture
def parent_auth(client):
    token = _signup(client, "parent@test.local", "secret123", "parent")
    return {"Authorization": f"Bearer {token}"}

@pytest.fixture
def child_auth(client):
    token = _signup(client, "child@test.local", "secret123", "child")
    return {"Authorization": f"Bearer {token}"}
