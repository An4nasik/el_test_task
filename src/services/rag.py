from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel, RunnablePassthrough
from src.services.llm import get_llm
from src.services.memory import get_memory
from src.knowledge.loader import load_vectorstore


_prompt = ChatPromptTemplate.from_messages([
    ("system", "Ты — доброжелательный литературный консультант. Отвечай кратко, опираясь на контекст."),
    ("human", "Вопрос: {question}\nКонтекст: {context}"),
])


def get_rag_chain(user_id: str):
    vectorstore = load_vectorstore()
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
    memory = get_memory(user_id)
    llm = get_llm()
    chain = (
        RunnableParallel({"context": retriever, "question": RunnablePassthrough()})
        | _prompt
        | llm
        | StrOutputParser()
    )
    chain = memory | chain
    return chain

