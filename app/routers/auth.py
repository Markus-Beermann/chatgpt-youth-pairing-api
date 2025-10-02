from fastapi import APIRouter, HTTPException, Depends, Request
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
import secrets

from app.deps import get_db
from app.models_db import User
from app.security.hashing import hash_password, verify_password
from app.security.jwt import create_access_token
from app.logging import log

router = APIRouter(prefix="/v1/auth", tags=["auth"])

class SignupIn(BaseModel):
    email: EmailStr
    password: str
    role: str  # "parent" | "child"

class LoginIn(BaseModel):
    email: EmailStr
    password: str

class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"

@router.post("/signup", response_model=TokenOut)
def signup(body: SignupIn, req: Request, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == body.email.lower()).first()
    if existing:
        raise HTTPException(status_code=409, detail="Email already exists")
    if body.role not in ("parent", "child"):
        raise HTTPException(status_code=400, detail="Invalid role")
    user_id = f"user_{secrets.token_hex(6)}"
    u = User(
        id=user_id,
        email=body.email.lower(),
        role=body.role,
        password_hash=hash_password(body.password),
    )
    db.add(u); db.commit()
    token = create_access_token(user_id=u.id, role=u.role)
    log("auth.signup", request_id=getattr(req.state, "request_id", None), user_id=u.id, role=u.role)
    return TokenOut(access_token=token)

@router.post("/login", response_model=TokenOut)
def login(body: LoginIn, req: Request, db: Session = Depends(get_db)):
    u = db.query(User).filter(User.email == body.email.lower()).first()
    if not u or not verify_password(body.password, u.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token(user_id=u.id, role=u.role)
    log("auth.login", request_id=getattr(req.state, "request_id", None), user_id=u.id)
    return TokenOut(access_token=token)
