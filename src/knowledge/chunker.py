from pathlib import Path

from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter


def load_documents(path: str) -> list:
    base_path = Path(path)
    files = list(base_path.glob("*.txt"))
    documents = []
    for file_path in files:
        loader = TextLoader(str(file_path), encoding="utf-8")
        documents.extend(loader.load())
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    return splitter.split_documents(documents)

