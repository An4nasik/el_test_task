from fastapi import Header, HTTPException, status

from src.core.config import settings


def verify_api_key(x_api_key: str = Header(..., alias="X-API-Key")) -> None:
    if x_api_key != settings.api_auth_key:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid API key")

