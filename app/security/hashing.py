from argon2 import PasswordHasher
from app.config import settings

ph = PasswordHasher()

def hash_code(code: str) -> str:
    return ph.hash(code + settings.pair_pepper)

def verify_code(code: str, code_hash: str) -> bool:
    try:
        ph.verify(code_hash, code + settings.pair_pepper)
        return True
    except Exception:
        return False

def hash_password(password: str) -> str:
    return ph.hash(password)

def verify_password(password: str, password_hash: str) -> bool:
    try:
        ph.verify(password_hash, password)
        return True
    except Exception:
        return False
