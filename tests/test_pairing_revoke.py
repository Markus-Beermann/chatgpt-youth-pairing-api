import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_revoke_pairing(client, parent_auth, child_auth):
    create = client.post("/v1/pairing/create", headers=parent_auth)
    code = create.json()["code"]

    claim = client.post("/v1/pairing/claim", headers=child_auth, json={"code": code})
    pairing_id = claim.json()["pairing_id"]

    revoke = client.delete(f"/v1/pairing/{pairing_id}", headers=parent_auth)
    assert revoke.status_code == 200
    assert revoke.json() == {"ok": True}

    listing = client.get("/v1/pairing", headers=child_auth)
    assert listing.status_code == 200
    assert any(p["pairing_id"] == pairing_id and p["status"] == "revoked" for p in listing.json())
