from langchain_openai import ChatOpenAI

from src.core.config import settings


def get_llm() -> ChatOpenAI:
    return ChatOpenAI(
        model=settings.ollama_chat_model,
        api_key=settings.ollama_api_key,
        base_url=settings.ollama_base_url,
        temperature=0.2,
    )
