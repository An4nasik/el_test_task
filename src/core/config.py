from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    app_name: str = "ai-book-consultant"
    app_env: str = "development"
    debug: bool = True

    api_auth_key: str
    api_base_url: str = "http://localhost:8000"

    postgres_host: str = "localhost"
    postgres_port: int = 5432
    postgres_user: str = "postgres"
    postgres_password: str = "postgres"
    postgres_db: str = "ai_consultant"
    database_url: str = ""

    rabbitmq_host: str = "localhost"
    rabbitmq_port: int = 5672
    rabbitmq_user: str = "guest"
    rabbitmq_password: str = "guest"
    rabbitmq_url: str = ""

    ollama_base_url: str = "https://ollama.com"
    ollama_api_key: str = ""
    ollama_chat_model: str = "gpt-oss:120b-cloud"
    ollama_vision_model: str = "qwen3-vl:2b-cloud"
    ollama_embedding_model: str = "all-minilm"

    telegram_bot_token: str = ""

    whisper_model: str = "tiny"

    vectorstore_path: str = "./data/vectorstore"
    knowledge_path: str = "./data/books"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

    def get_database_url(self) -> str:
        if self.database_url:
            return self.database_url
        return f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"

    def get_rabbitmq_url(self) -> str:
        if self.rabbitmq_url:
            return self.rabbitmq_url
        return f"amqp://{self.rabbitmq_user}:{self.rabbitmq_password}@{self.rabbitmq_host}:{self.rabbitmq_port}/"


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
