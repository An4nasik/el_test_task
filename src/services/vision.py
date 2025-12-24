import base64

from langchain_core.messages import HumanMessage
from langchain_ollama import ChatOllama

from src.core.config import settings


def describe_image(image_bytes: bytes) -> str:
    b64 = base64.b64encode(image_bytes).decode()
    llm = ChatOllama(
        model=settings.ollama_vision_model,
        base_url=settings.ollama_base_url,
    )
    message = HumanMessage(
        content=[
            {"type": "text", "text": "Опиши изображение"},
            {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{b64}"}},
        ]
    )
    response = llm.invoke([message])
    return response.content
