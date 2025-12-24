from pathlib import Path
from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaEmbeddings
from src.core.config import settings
from src.knowledge.vectorizer import build_vectorstore

_vectorstore: FAISS | None = None


def load_vectorstore() -> FAISS:
    global _vectorstore
    if _vectorstore:
        return _vectorstore
    path = Path(settings.vectorstore_path)
    embeddings = OllamaEmbeddings(model=settings.ollama_embedding_model, base_url=settings.ollama_base_url, api_key=settings.ollama_api_key)
    if path.exists():
        _vectorstore = FAISS.load_local(path, embeddings, allow_dangerous_deserialization=True)
    else:
        _vectorstore = build_vectorstore()
    return _vectorstore

