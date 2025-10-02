import sys, os, pytest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_parent_create_rate_limit():
    """
    A parent can only create up to 5 codes per minute.
    On the 6th attempt, the API should return 429 Too Many Requests.
    """
    headers = {"x-demo-role": "parent", "x-demo-user": "u_parent_limit"}

    # Do 5 successful creates
    for i in range(5):
        resp = client.post("/v1/pairing/create", headers=headers)
        assert resp.status_code == 200

    # 6th should fail
    resp = client.post("/v1/pairing/create", headers=headers)
    assert resp.status_code == 429
    assert "Too many requests" in resp.text
