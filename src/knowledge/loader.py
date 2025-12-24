from pathlib import Path

from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

from src.core.config import settings
from src.knowledge.vectorizer import build_vectorstore

INDEX_FILE_NAME = "index.faiss"
METADATA_FILE_NAME = "index.pkl"

_vectorstore: FAISS | None = None


def load_vectorstore() -> FAISS:
    global _vectorstore
    if _vectorstore:
        return _vectorstore
    path = Path(settings.vectorstore_path)

    if settings.use_local_embeddings:
        embeddings = HuggingFaceEmbeddings(model_name=settings.local_embedding_model)
    else:
        api_key = settings.openai_api_key
        base_url = settings.openai_base_url
        model = settings.openai_embedding_model

        # Fallback to Ollama/OpenRouter if OpenAI key is not set or is a placeholder
        if not api_key or api_key == "your_openai_api_key":
            api_key = settings.ollama_api_key
            base_url = settings.ollama_base_url
            model = settings.ollama_embedding_model

        embeddings = OpenAIEmbeddings(
            model=model,
            api_key=api_key,
            base_url=base_url,
        )

    index_file = path / INDEX_FILE_NAME
    metadata_file = path / METADATA_FILE_NAME
    if path.exists() and index_file.exists() and metadata_file.exists():
        _vectorstore = FAISS.load_local(path, embeddings, allow_dangerous_deserialization=True)
    else:
        _vectorstore = build_vectorstore()
    return _vectorstore
