# Placeholder for real JWT auth (future work)
from fastapi import APIRouter

router = APIRouter(prefix="/v1/auth", tags=["auth"])

@router.get("/ping")
def ping():
    return {"ok": True}
