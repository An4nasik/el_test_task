from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.database import get_session


def get_db(session: AsyncSession = Depends(get_session)) -> AsyncSession:  # noqa: B008
    return session
