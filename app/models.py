from pydantic import BaseModel
from datetime import datetime

class PairingCreateOut(BaseModel):
    code: str
    expires_at: datetime
    qr_deeplink: str | None = None

class PairingClaimIn(BaseModel):
    code: str

class PairingOut(BaseModel):
    pairing_id: str
    parent_id: str
    child_id: str
    status: str
