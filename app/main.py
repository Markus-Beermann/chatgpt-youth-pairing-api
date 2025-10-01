from fastapi import FastAPI
from app.routers import pairing, auth

app = FastAPI(title="ChatGPT Youth – Pairing API (v0)")

app.include_router(auth.router)
app.include_router(pairing.router)

@app.get("/")
def root():
    return {"service": "youth-pairing-api", "version": "v0"}
