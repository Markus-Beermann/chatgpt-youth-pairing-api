import sys, os, pytest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_parent_create_rate_limit(client, parent_auth):
    for _ in range(5):
        ok = client.post("/v1/pairing/create", headers=parent_auth)
        assert ok.status_code == 200
    r = client.post("/v1/pairing/create", headers=parent_auth)
    assert r.status_code == 429

