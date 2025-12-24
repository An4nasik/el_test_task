from langchain_community.vectorstores import FAISS
from src.knowledge.loader import load_vectorstore


def get_retriever(k: int = 3):
    vectorstore: FAISS = load_vectorstore()
    return vectorstore.as_retriever(search_kwargs={"k": k})

