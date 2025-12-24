from fastapi import Depends, Header, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.config import settings
from src.db.database import get_session


def verify_api_key(x_api_key: str = Header(..., alias="X-API-Key")) -> None:
    if x_api_key != settings.api_auth_key:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid API key")


def get_db(session: AsyncSession = Depends(get_session)) -> AsyncSession:
    return session
