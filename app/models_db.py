from sqlalchemy import Column, String, DateTime, Integer
from app.database import Base

class PairingCode(Base):
    __tablename__ = "pairing_codes"

    id = Column(String, primary_key=True, index=True)   # code_id
    parent_id = Column(String, index=True)
    hash = Column(String, nullable=False)
    exp = Column(DateTime, nullable=False)
    used_at = Column(DateTime, nullable=True)
    failures = Column(Integer, default=0)

class Pairing(Base):
    __tablename__ = "pairings"

    id = Column(String, primary_key=True, index=True)   # pairing_id
    parent_id = Column(String, index=True)
    child_id = Column(String, index=True)
    status = Column(String, default="active")
