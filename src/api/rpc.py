from typing import Any

from faststream.rabbit import RabbitBroker

from src.core.config import settings

rpc_broker = RabbitBroker(settings.get_rabbitmq_url())
RPC_TIMEOUT_SECONDS = 30


async def start_rpc() -> None:
    await rpc_broker.connect()


async def stop_rpc() -> None:
    await rpc_broker.stop()


async def rpc_text(payload: dict[str, Any]) -> str:
    # Используем request() вместо publish(rpc=True) для RPC вызовов
    msg = await rpc_broker.request(payload, queue="ai.text", timeout=RPC_TIMEOUT_SECONDS)
    result = msg.body
    if isinstance(result, bytes):
        return result.decode()
    if not isinstance(result, str):
        return str(result)
    return result


async def rpc_audio(payload: dict[str, Any]) -> str:
    # Используем request() вместо publish(rpc=True) для RPC вызовов
    msg = await rpc_broker.request(payload, queue="ai.audio", timeout=RPC_TIMEOUT_SECONDS)
    result = msg.body
    if isinstance(result, bytes):
        return result.decode()
    if not isinstance(result, str):
        return str(result)
    return result
