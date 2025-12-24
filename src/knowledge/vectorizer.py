from pathlib import Path

from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

from src.core.config import settings
from src.knowledge.chunker import load_documents


def build_vectorstore(data_path: str | None = None, store_path: str | None = None) -> FAISS:
    docs_path = data_path or settings.knowledge_path
    faiss_path = store_path or settings.vectorstore_path
    documents = load_documents(docs_path)

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

    vectorstore = FAISS.from_documents(documents, embeddings)
    Path(faiss_path).mkdir(parents=True, exist_ok=True)
    vectorstore.save_local(faiss_path)
    return vectorstore
