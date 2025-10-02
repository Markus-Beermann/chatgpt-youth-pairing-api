# app/config.py
from dotenv import load_dotenv; load_dotenv()
import os
from pydantic import BaseModel

class Settings(BaseModel):
    app_env: str = os.getenv("APP_ENV", "dev")
    pair_pepper: str = os.getenv("PAIR_PEPPER", "CHANGE_ME")
    jwt_secret: str = os.getenv("JWT_SECRET", "CHANGE_ME")
    jwt_expire_min: int = int(os.getenv("JWT_EXPIRE_MIN", "60"))

settings = Settings()
