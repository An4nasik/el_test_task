from langchain_community.chat_models import ChatOllama

from src.core.config import settings


def get_llm() -> ChatOllama:
    return ChatOllama(
        model=settings.ollama_chat_model,
        base_url=settings.ollama_base_url,
        temperature=0.2,
    )
