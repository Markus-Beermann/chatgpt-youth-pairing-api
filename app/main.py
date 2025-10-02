from fastapi import FastAPI
import uuid

from app.database import Base, engine
from app.models_db import User, PairingCode, Pairing  # ensure models are imported
from app.routers import auth, pairing

app = FastAPI(title="ChatGPT Youth Pairing API")

# Request ID middleware
@app.middleware("http")
async def add_request_id(request, call_next):
    request.state.request_id = str(uuid.uuid4())
    return await call_next(request)

# Create DB tables
Base.metadata.create_all(bind=engine)

# Routers
app.include_router(auth.router)
app.include_router(pairing.router)
