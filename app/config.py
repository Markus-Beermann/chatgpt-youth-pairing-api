# app/config.py
from dotenv import load_dotenv

load_dotenv()  # <-- .env einlesen, bevor os.getenv verwendet wird

from pydantic import BaseModel
import os

class Settings(BaseModel):
    app_env: str = os.getenv("APP_ENV", "dev")
    pair_pepper: str = os.getenv("PAIR_PEPPER", "CHANGE_THIS_TO_A_LONG_RANDOM_STRING")
    redis_url: str | None = os.getenv("REDIS_URL")

settings = Settings()
