from langchain_ollama import ChatOllama
from src.core.config import settings


def get_llm() -> ChatOllama:
    return ChatOllama(
        model=settings.ollama_chat_model,
        base_url=settings.ollama_base_url,
        api_key=settings.ollama_api_key,
        temperature=0.2,
    )
