# Minimal in-memory rate limiter for demo purposes.
# Replace with Redis-based token bucket for production.

import time
from typing import Dict, Tuple

# key -> (count, reset_ts)
WINDOWS: Dict[str, Tuple[int, float]] = {}

def allow(key: str, limit: int, window_seconds: int) -> bool:
    now = time.time()
    count, reset = WINDOWS.get(key, (0, now + window_seconds))
    if now > reset:
        count, reset = 0, now + window_seconds
    if count + 1 > limit:
        WINDOWS[key] = (count, reset)
        return False
    WINDOWS[key] = (count + 1, reset)
    return True
