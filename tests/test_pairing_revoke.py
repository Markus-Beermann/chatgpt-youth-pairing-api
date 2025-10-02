import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_revoke_pairing():
    """
    Parent creates a code, child claims it, parent revokes it.
    API should respond with {"ok": true}, and status of pairing becomes 'revoked'.
    """
    parent_headers = {"x-demo-role": "parent", "x-demo-user": "u_parent_revoke"}
    child_headers = {"x-demo-role": "child", "x-demo-user": "u_child_revoke"}

    # 1. Parent creates a pairing code
    create = client.post("/v1/pairing/create", headers=parent_headers)
    assert create.status_code == 200
    code = create.json()["code"]

    # 2. Child claims the code
    claim = client.post("/v1/pairing/claim", headers=child_headers, json={"code": code})
    assert claim.status_code == 200
    pairing_id = claim.json()["pairing_id"]

    # 3. Parent revokes the pairing
    revoke = client.delete(f"/v1/pairing/{pairing_id}", headers=parent_headers)
    assert revoke.status_code == 200
    assert revoke.json() == {"ok": True}

    # 4. Verify the pairing shows as revoked in list
    listing = client.get("/v1/pairing", headers=child_headers)
    assert listing.status_code == 200
    data = listing.json()
    assert any(p["pairing_id"] == pairing_id and p["status"] == "revoked" for p in data)
