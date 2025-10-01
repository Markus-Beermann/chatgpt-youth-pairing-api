# In-memory stores for v0 (replace with real DB in v1)
from typing import Dict, Any, List

USERS: Dict[str, Dict[str, Any]] = {}
PAIRINGS: List[Dict[str, Any]] = []
CODES: Dict[str, Dict[str, Any]] = {}  # key: code_id -> {parent_id, hash, exp, used_at, failures}
