import uuid
from starlette.middleware.base import BaseHTTPMiddleware
from app.database import Base, engine
# Create DB tables
Base.metadata.create_all(bind=engine)

from fastapi import FastAPI
from app.routers import pairing, auth

app = FastAPI(title="ChatGPT Youth – Pairing API (v0)")

# Create DB tables
Base.metadata.create_all(bind=engine)

@app.middleware("http")
async def add_request_id(request, call_next):
    request.state.request_id = str(uuid.uuid4())
    return await call_next(request)

app.include_router(auth.router)
app.include_router(pairing.router)

@app.get("/")
def root():
    return {"service": "youth-pairing-api", "version": "v0"}
