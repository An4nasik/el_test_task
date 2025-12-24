from pathlib import Path

from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

from src.core.config import settings
from src.knowledge.vectorizer import build_vectorstore

_vectorstore: FAISS | None = None


def load_vectorstore() -> FAISS:
    global _vectorstore
    if _vectorstore:
        return _vectorstore
    path = Path(settings.vectorstore_path)
    embeddings = OpenAIEmbeddings(
        model=settings.openai_embedding_model,
        api_key=settings.openai_api_key,
        base_url=settings.openai_base_url,
    )
    index_file = path / "index.faiss"
    metadata_file = path / "index.pkl"
    if index_file.exists() and metadata_file.exists():
        _vectorstore = FAISS.load_local(path, embeddings, allow_dangerous_deserialization=True)
    else:
        _vectorstore = build_vectorstore()
    return _vectorstore
