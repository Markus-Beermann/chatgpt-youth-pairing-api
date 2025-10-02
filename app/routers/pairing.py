# app/routers/pairing.py
from fastapi import APIRouter, Depends, HTTPException, Request, Query
from datetime import datetime, timedelta, timezone
import secrets
import re

from app.deps import require_role
from app.security.hashing import hash_code, verify_code
from app.security.rate_limit import allow
from app.models import PairingCreateOut, PairingClaimIn, PairingOut, RevokeOut
from app.db import CODES, PAIRINGS
from app.logging import log  # if you renamed to jsonlog.py, change to: from app.jsonlog import log

router = APIRouter(prefix="/v1/pairing", tags=["pairing"])

# Default TTL (minutes) used when no explicit ?ttl= is provided
CODE_TTL_MIN = 10

# Accept codes like '9CBD-621' (4 alnum, dash, 3 alnum)
CODE_RE = re.compile(r"^[A-Z0-9]{4}-[A-Z0-9]{3}$")


def _now() -> datetime:
    """Return current UTC time."""
    return datetime.now(timezone.utc)


@router.post("/create", response_model=PairingCreateOut)
async def create_pairing_code(
    req: Request,
    parent=Depends(require_role("parent")),
    ttl: int | None = Query(
        None, ge=1, le=600, description="Optional TTL in seconds (1..600)"
    ),
):
    """
    Generate a short-lived pairing code for a parent.
    Optional ?ttl= seconds to override the default (10 minutes).
    """
    request_id = getattr(req.state, "request_id", None)

    # Rate limit: per parent per minute
    rl_key = f"pair:create:{parent['id']}"
    if not allow(rl_key, limit=5, window_seconds=60):
        raise HTTPException(status_code=429, detail="Too many requests")

    # Generate code like "9CBD-621"
    code = f"{secrets.token_hex(2).upper()}-{secrets.randbelow(1000):03d}"
    code = code.replace("0", "Z")  # avoid visually confusing zeros

    # Expiration
    expires = _now() + (
        timedelta(seconds=ttl) if ttl is not None else timedelta(minutes=CODE_TTL_MIN)
    )

    code_id = secrets.token_hex(8)
    CODES[code_id] = {
        "parent_id": parent["id"],
        "hash": hash_code(code),
        "exp": expires,
        "used_at": None,
        "failures": 0,
    }

    deeplink = f"youthapp://pair?c={code.replace('-', '')}"
    log(
        "pairing.code.created",
        request_id=request_id,
        actor_user_id=parent["id"],
        code_id=code_id,
        expires_at=expires.isoformat(),
    )
    return PairingCreateOut(code=code, expires_at=expires, qr_deeplink=deeplink)


@router.post("/claim", response_model=PairingOut)
async def claim_pairing(
    payload: PairingClaimIn, req: Request, child=Depends(require_role("child"))
):
    """
    Claim a valid, unused, unexpired code as a child.
    """
    request_id = getattr(req.state, "request_id", None)

    # Rate limit: per child per minute
    rl_key = f"pair:claim:{child['id']}"
    if not allow(rl_key, limit=10, window_seconds=60):
        raise HTTPException(status_code=429, detail="Too many requests")

    code = payload.code.strip().upper()
    if not CODE_RE.match(code):
        raise HTTPException(status_code=400, detail="Invalid or expired code")

    # Match any non-used, non-expired code
    matched = None
    now = _now()
    for code_id, rec in CODES.items():
        if rec["used_at"] is None and now < rec["exp"] and verify_code(code, rec["hash"]):
            matched = (code_id, rec)
            break

    if not matched:
        # Forensics-friendly, PII-safe log
        log(
            "pairing.claim.attempt",
            request_id=request_id,
            actor_user_id=child["id"],
            result="fail",
            reason="no_match",
        )
        raise HTTPException(status_code=400, detail="Invalid or expired code")

    code_id, rec = matched
    rec["used_at"] = now

    pairing_id = f"pair_{len(PAIRINGS)+1}"
    PAIRINGS.append(
        {"id": pairing_id, "parent": rec["parent_id"], "child": child["id"], "status": "active"}
    )
    log(
        "pairing.claim.success",
        request_id=request_id,
        actor_user_id=child["id"],
        code_id=code_id,
        pairing_id=pairing_id,
    )

    return PairingOut(
        pairing_id=pairing_id,
        parent_id=rec["parent_id"],
        child_id=child["id"],
        status="active",
    )


@router.get("", response_model=list[PairingOut])
async def list_pairings(req: Request, actor=Depends(require_role("child"))):
    """
    List pairings visible to the current actor (child or parent in this demo).
    """
    request_id = getattr(req.state, "request_id", None)

    res: list[PairingOut] = []
    for p in PAIRINGS:
        if p["child"] == actor["id"] or p["parent"] == actor["id"]:
            res.append(
                PairingOut(
                    pairing_id=p["id"], parent_id=p["parent"], child_id=p["child"], status=p["status"]
                )
            )
    log("pairing.list", request_id=request_id, actor_user_id=actor["id"], count=len(res))
    return res


@router.delete("/{pairing_id}", response_model=RevokeOut)
async def revoke_pairing(
    pairing_id: str, req: Request, actor=Depends(require_role("parent"))
):
    """
    Revoke an existing pairing (parent-initiated).
    """
    request_id = getattr(req.state, "request_id", None)

    for p in PAIRINGS:
        if p["id"] == pairing_id and p["parent"] == actor["id"]:
            p["status"] = "revoked"
            log(
                "pairing.revoked",
                request_id=request_id,
                actor_user_id=actor["id"],
                pairing_id=pairing_id,
            )
            return RevokeOut(ok=True)

    raise HTTPException(status_code=404, detail="Pairing not found")