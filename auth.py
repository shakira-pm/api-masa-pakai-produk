from typing import Annotated
from fastapi import Header, HTTPException, status

# Kunci contoh untuk praktikum. Jangan gunakan kunci ini untuk sistem produksi.
API_KEYS = {
    "admin-demo-123": "admin",
    "student-demo-123": "student",
}

def get_current_user(x_api_key: Annotated[str | None, Header()] = None):
    if not x_api_key or x_api_key not in API_KEYS:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API key tidak ada atau tidak valid.",
        )
    return {"role": API_KEYS[x_api_key]}

def require_admin(user=__import__("fastapi").Depends(get_current_user)):
    if user["role"] != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Akses hanya untuk Admin.",
        )
    return user
