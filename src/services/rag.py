from operator import itemgetter

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableParallel
from langchain_core.runnables.history import RunnableWithMessageHistory

from src.knowledge.loader import load_vectorstore
from src.services.llm import get_llm
from src.services.memory import get_history

_prompt = ChatPromptTemplate.from_messages([
    ("system", "Ты — доброжелательный литературный консультант. Отвечай кратко, опираясь на контекст."),
    MessagesPlaceholder(variable_name="history"),
    ("human", "Вопрос: {question}\nКонтекст: {context}"),
])


def get_rag_chain():
    vectorstore = load_vectorstore()
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
    llm = get_llm()
    chain = (
        RunnableParallel(
            {
                "context": itemgetter("question") | retriever,
                "question": itemgetter("question"),
            }
        )
        | _prompt
        | llm
        | StrOutputParser()
    )
    return RunnableWithMessageHistory(
        chain,
        get_history,
        input_messages_key="question",
        history_messages_key="history",
    )
