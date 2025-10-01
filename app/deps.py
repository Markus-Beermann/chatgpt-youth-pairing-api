from fastapi import Header, HTTPException

# Demo auth: inject user via headers
def require_role(expected_role: str):
    async def dep(x_demo_role: str = Header(None), x_demo_user: str = Header(None)):
        if x_demo_role != expected_role or not x_demo_user:
            raise HTTPException(status_code=401, detail="Unauthorized (demo headers missing or wrong role)")
        return {"id": x_demo_user, "role": x_demo_role}
    return dep
