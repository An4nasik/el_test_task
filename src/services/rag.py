from __future__ import annotations

import asyncio
import logging
from typing import Any, List, Optional

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableMap

from src.knowledge.loader import load_vectorstore
from src.services.llm import get_llm

logger = logging.getLogger(__name__)

# Очень простой prompt
_PROMPT = ChatPromptTemplate.from_messages([
    ("system", "Ты — литературный консультант. Отвечай кратко и по делу."),
    ("human", "Вопрос: {question}\nКонтекст: {context}"),
])


def _docs_to_context(docs: List[Any], max_chars: int = 2000) -> str:
    parts: List[str] = []
    for d in docs:
        text = getattr(d, "page_content", None)
        if text is None:
            try:
                text = str(d)
            except Exception:
                text = ""
        # заменяем переносы и лишние пробелы
        text = text.replace("\r", " ").replace("\n", " ")
        text = " ".join(text.split())
        if text:
            parts.append(text)

    joined = "\n---\n".join(parts)
    if len(joined) > max_chars:
        return joined[: max_chars - 3].rstrip() + "..."
    return joined


def get_rag_chain(k: int = 3, max_context_chars: int = 2000) -> Any:
    """Простая RAG-цепочка.

    Реализация минималистична и безопасна:
    - Загружаем vectorstore один раз.
    - При поиске используем async-метод vectorstore.asimilarity_search если он есть,
      иначе вызываем синхронный vectorstore.similarity_search в executor.
    - В retriever передаётся только строка вопроса.
    """
    vectorstore = load_vectorstore()
    llm = get_llm()

    async def _retrieve(input_mapping: dict) -> List[Any]:
        # Извлекаем вопрос как строку и защищаемся от dict
        q = input_mapping.get("question")
        if q is None:
            return []
        if not isinstance(q, str):
            q = str(q)

        loop = asyncio.get_running_loop()
        try:
            if hasattr(vectorstore, "asimilarity_search"):
                docs = await vectorstore.asimilarity_search(q, k=k)
            else:
                # sync variant -> run in executor
                docs = await loop.run_in_executor(None, lambda: vectorstore.similarity_search(q, k=k))
            logger.debug("Retriever returned %d docs for question=%s", len(docs) if docs else 0, q)
            return docs or []
        except Exception as exc:
            logger.exception("Error while querying vectorstore: %s", exc)
            return []

    def _map_docs(input_mapping: dict) -> str:
        docs = input_mapping.get("context")
        if docs is None:
            return ""
        if not isinstance(docs, list):
            docs = [docs]
        return _docs_to_context(docs, max_chars=max_context_chars)

    chain = (
        RunnableMap({
            "context": _retrieve,
            "question": (lambda inp: str(inp.get("question", ""))),
        })
        | RunnableMap({
            "context": _map_docs,
            "question": (lambda q: str(q) if not isinstance(q, str) else q),
        })
        | _PROMPT
        | llm
        | StrOutputParser()
    )

    return chain


# Маленький example helper (не запускает сеть) — удобен для локальной отладки
def example_usage_sync(question: str, retriever: Optional[Any] = None, llm: Optional[Any] = None) -> str:
    """Пример синхронного вызова цепочки (обёртка вокруг asyncio.run для удобства).

    Используй это в локальной отладке. Возвращает строковый ответ от цепочки.
    """
    chain = get_rag_chain(retriever=retriever, llm=llm)
    return asyncio.run(chain.ainvoke({"question": question}))
