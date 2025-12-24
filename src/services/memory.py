from typing import Dict
from langchain_core.chat_history import InMemoryChatMessageHistory, BaseChatMessageHistory
from langchain_core.messages import BaseMessage

_history_store: Dict[str, InMemoryChatMessageHistory] = {}


def get_history(session_id: str) -> BaseChatMessageHistory:
    history = _history_store.setdefault(session_id, InMemoryChatMessageHistory())
    if len(history.messages) > 10:
        history.messages = history.messages[-10:]
    return history


def clear_history(session_id: str) -> None:
    if session_id in _history_store:
        del _history_store[session_id]


def add_message(session_id: str, message: BaseMessage) -> None:
    history = get_history(session_id)
    history.add_message(message)
