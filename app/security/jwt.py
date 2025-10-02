import time
import jwt
from typing import TypedDict, Literal
from app.config import settings

Algorithm = Literal["HS256"]
ALGO: Algorithm = "HS256"

class JWTClaims(TypedDict):
    sub: str
    role: str
    exp: int
    iat: int

def create_access_token(user_id: str, role: str, expire_minutes: int | None = None) -> str:
    now = int(time.time())
    exp = now + 60 * (expire_minutes or settings.jwt_expire_min)
    payload: JWTClaims = {"sub": user_id, "role": role, "iat": now, "exp": exp}
    return jwt.encode(payload, settings.jwt_secret, algorithm=ALGO)

def decode_token(token: str) -> JWTClaims:
    return jwt.decode(token, settings.jwt_secret, algorithms=[ALGO])
