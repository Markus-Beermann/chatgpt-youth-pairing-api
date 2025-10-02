import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.main import app
from fastapi.testclient import TestClient

# tests/test_pairing.py
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_and_claim_pairing():
    # Parent creates code
    resp = client.post("/v1/pairing/create", headers={
        "x-demo-role": "parent",
        "x-demo-user": "u_parent_1"
    })
    assert resp.status_code == 200
    code = resp.json()["code"]

    # Child redeems code
    resp = client.post("/v1/pairing/claim",
                       headers={"x-demo-role": "child", "x-demo-user": "u_child_1"},
                       json={"code": code})
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "active"
    assert data["parent_id"] == "u_parent_1"
    assert data["child_id"] == "u_child_1"

    # Child see Pairing in list
    resp = client.get("/v1/pairing", headers={
        "x-demo-role": "child",
        "x-demo-user": "u_child_1"
    })
    assert resp.status_code == 200
    assert any(p["child_id"] == "u_child_1" for p in resp.json())
