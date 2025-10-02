from fastapi import Header, HTTPException, Depends
from typing import Annotated
from sqlalchemy.orm import Session
import jwt

from app.database import SessionLocal
from app.models_db import User
from app.security.jwt import decode_token

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(authorization: Annotated[str | None, Header()] = None,
                     db: Session = Depends(get_db)) -> User:
    if not authorization or not authorization.lower().startswith("bearer "):
        raise HTTPException(status_code=401, detail="Missing Bearer token")
    token = authorization.split(" ", 1)[1]
    try:
        claims = decode_token(token)
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = db.get(User, claims["sub"])
    if not user:
        raise HTTPException(status_code=401, detail="Unknown user")
    return user

def require_role(role: str):
    def _dep(user: User = Depends(get_current_user)):
        if user.role != role:
            raise HTTPException(status_code=403, detail="Forbidden")
        return {"id": user.id, "role": user.role, "email": user.email}
    return _dep
