import sys, os, time
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_invalid_code_rejected():
    """Claiming a code that never existed should fail."""
    resp = client.post("/v1/pairing/claim",
                       headers={"x-demo-role": "child", "x-demo-user": "u_child_x"},
                       json={"code": "ZZZ-999"})
    assert resp.status_code == 400


def test_already_claimed_code_rejected():
    """A pairing code can only be claimed once."""
    # Parent creates a code
    create = client.post("/v1/pairing/create",
                         headers={"x-demo-role": "parent", "x-demo-user": "u_parent_2"})
    code = create.json()["code"]

    # Child claims once → OK
    claim1 = client.post("/v1/pairing/claim",
                         headers={"x-demo-role": "child", "x-demo-user": "u_child_2"},
                         json={"code": code})
    assert claim1.status_code == 200

    # Child tries again → FAIL
    claim2 = client.post("/v1/pairing/claim",
                         headers={"x-demo-role": "child", "x-demo-user": "u_child_2"},
                         json={"code": code})
    assert claim2.status_code == 400
    assert "Invalid or expired code" in claim2.text


def test_expired_code_rejected():
    """A code that has passed its TTL should be rejected."""
    # Parent creates a code with a very short TTL
    create = client.post("/v1/pairing/create?ttl=1",  # query param sets TTL=1 second
                         headers={"x-demo-role": "parent", "x-demo-user": "u_parent_3"})
    code = create.json()["code"]

    # Wait for expiration
    time.sleep(2)

    # Try to claim after expiration
    resp = client.post("/v1/pairing/claim",
                       headers={"x-demo-role": "child", "x-demo-user": "u_child_3"},
                       json={"code": code})
    assert resp.status_code == 400
    assert "Invalid or expired code" in resp.text
