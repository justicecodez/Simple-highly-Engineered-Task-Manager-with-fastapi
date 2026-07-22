from fastapi import HTTPException

def authorize(allowed: bool):
    if not allowed:
        raise HTTPException(
            status_code=403,
            detail="Forbidden",
        )