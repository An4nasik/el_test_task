import base64

from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI

from src.core.config import settings


def _get_vision_llm() -> ChatOpenAI:
    return ChatOpenAI(
        model=settings.ollama_vision_model,
        api_key=settings.ollama_api_key,
        base_url=settings.ollama_base_url,
    )


def describe_image(image_bytes: bytes) -> str:
    """Synchronous version for backward compatibility."""
    b64 = base64.b64encode(image_bytes).decode()
    llm = _get_vision_llm()
    message = HumanMessage(
        content=[
            {"type": "text", "text": "Опиши изображение"},
            {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{b64}"}},
        ]
    )
    response = llm.invoke([message])
    return response.content


async def describe_image_async(image_bytes: bytes) -> str:
    """Asynchronous version for use in async routes."""
    b64 = base64.b64encode(image_bytes).decode()
    llm = _get_vision_llm()
    message = HumanMessage(
        content=[
            {"type": "text", "text": "Опиши изображение"},
            {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{b64}"}},
        ]
    )
    response = await llm.ainvoke([message])
    return response.content
