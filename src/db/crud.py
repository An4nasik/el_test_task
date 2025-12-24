from datetime import datetime
from typing import Sequence

from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models import Conversation, Message


async def save_message(session: AsyncSession, user_id: str, role: str, content: str) -> Message:
    conversation = await _get_or_create_conversation(session, user_id)
    message = Message(conversation_id=conversation.id, role=role, content=content, created_at=datetime.utcnow())
    session.add(message)
    await session.commit()
    await session.refresh(message)
    return message


async def get_conversation_history(session: AsyncSession, user_id: str, limit: int = 10) -> Sequence[Message]:
    stmt = (
        select(Message)
        .join(Conversation)
        .where(Conversation.user_id == user_id)
        .order_by(Message.created_at.desc())
        .limit(limit)
    )
    result = await session.execute(stmt)
    messages = list(result.scalars())
    return list(reversed(messages))


async def clear_conversation(session: AsyncSession, user_id: str) -> None:
    stmt = delete(Conversation).where(Conversation.user_id == user_id)
    await session.execute(stmt)
    await session.commit()


async def _get_or_create_conversation(session: AsyncSession, user_id: str) -> Conversation:
    stmt = select(Conversation).where(Conversation.user_id == user_id).limit(1)
    result = await session.execute(stmt)
    conversation = result.scalar_one_or_none()
    if conversation:
        return conversation
    conversation = Conversation(user_id=user_id, created_at=datetime.utcnow())
    session.add(conversation)
    await session.commit()
    await session.refresh(conversation)
    return conversation

