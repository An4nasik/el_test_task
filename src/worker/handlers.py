import base64
from typing import Any, Dict

from faststream import ContextRepo
from faststream.rabbit import RabbitMessage

from src.services.rag import get_rag_chain
from src.services.vision import describe_image
from src.services.memory import add_message
from langchain_core.messages import HumanMessage, AIMessage


async def _maybe_describe_image(image_base64: str | None) -> str:
    if not image_base64:
        return ""
    image_bytes = base64.b64decode(image_base64)
    return describe_image(image_bytes)


def _combine_context(text: str, image_desc: str) -> str:
    if image_desc:
        return f"Текст: {text}\nОписание изображения: {image_desc}"
    return text


async def handle_text(payload: Dict[str, Any], message: RabbitMessage, context: ContextRepo) -> str:
    user_id = payload["user_id"]
    text = payload.get("text", "")
    image_desc = payload.get("image_desc", "")

    question = _combine_context(text, image_desc)

    chain = get_rag_chain(user_id)
    answer = await chain.ainvoke(question)

    add_message(user_id, HumanMessage(content=question))
    add_message(user_id, AIMessage(content=answer))
    return answer


async def handle_audio(payload: Dict[str, Any], message: RabbitMessage, context: ContextRepo) -> str:
    user_id = payload["user_id"]
    text = payload.get("text", "")
    image_desc = payload.get("image_desc", "")

    question = _combine_context(text, image_desc)

    chain = get_rag_chain(user_id)
    answer = await chain.ainvoke(question)

    add_message(user_id, HumanMessage(content=question))
    add_message(user_id, AIMessage(content=answer))
    return answer
