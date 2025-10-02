import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.main import app
from fastapi.testclient import TestClient

# tests/test_pairing.py
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_and_claim_pairing(client, parent_auth, child_auth):
    # Parent creates code
    resp = client.post("/v1/pairing/create", headers=parent_auth)
    assert resp.status_code == 200
    code = resp.json()["code"]

    # Child claims
    resp = client.post("/v1/pairing/claim", headers=child_auth, json={"code": code})
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "active"
