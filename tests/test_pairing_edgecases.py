import time

def test_invalid_code_rejected(client, child_auth):
    r = client.post("/v1/pairing/claim", headers=child_auth, json={"code": "ZZZ-999"})
    assert r.status_code == 400

def test_already_claimed_code_rejected(client, parent_auth, child_auth):
    create = client.post("/v1/pairing/create", headers=parent_auth)
    code = create.json()["code"]

    claim1 = client.post("/v1/pairing/claim", headers=child_auth, json={"code": code})
    assert claim1.status_code == 200

    claim2 = client.post("/v1/pairing/claim", headers=child_auth, json={"code": code})
    assert claim2.status_code == 400
    assert "Invalid or expired code" in claim2.text

def test_expired_code_rejected(client, parent_auth, child_auth):
    create = client.post("/v1/pairing/create?ttl=1", headers=parent_auth)
    code = create.json()["code"]
    time.sleep(2)
    r = client.post("/v1/pairing/claim", headers=child_auth, json={"code": code})
    assert r.status_code == 400
    assert "Invalid or expired code" in r.text
