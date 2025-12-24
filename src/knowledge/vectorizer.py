from pathlib import Path

from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OllamaEmbeddings

from src.core.config import settings
from src.knowledge.chunker import load_documents


def build_vectorstore(data_path: str | None = None, store_path: str | None = None) -> FAISS:
    docs_path = data_path or settings.knowledge_path
    faiss_path = store_path or settings.vectorstore_path
    documents = load_documents(docs_path)
    embeddings = OllamaEmbeddings(
        model=settings.ollama_embedding_model,
        base_url=settings.ollama_base_url,
    )
    vectorstore = FAISS.from_documents(documents, embeddings)
    Path(faiss_path).mkdir(parents=True, exist_ok=True)
    vectorstore.save_local(faiss_path)
    return vectorstore
