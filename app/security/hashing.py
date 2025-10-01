from argon2 import PasswordHasher
from app.config import settings

ph = PasswordHasher()

def hash_code(code: str) -> str:
    return ph.hash(code + settings.pair_pepper)

def verify_code(code: str, code_hash: str) -> bool:
    try:
        return ph.verify(code_hash, code + settings.pair_pepper) is None or True
    except Exception:
        return False
