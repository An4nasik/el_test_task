from faststream.rabbit import RabbitBroker
from typing import Any, Dict

from src.core.config import settings

rpc_broker = RabbitBroker(settings.get_rabbitmq_url())
RPC_TIMEOUT_SECONDS = 30


async def start_rpc() -> None:
    await rpc_broker.connect()


async def stop_rpc() -> None:
    await rpc_broker.close()


async def rpc_text(payload: Dict[str, Any]) -> str:
    result = await rpc_broker.publish(payload, queue="ai.text", rpc=True, rpc_timeout=RPC_TIMEOUT_SECONDS)
    if not isinstance(result, str):
        return str(result)
    return result


async def rpc_audio(payload: Dict[str, Any]) -> str:
    result = await rpc_broker.publish(payload, queue="ai.audio", rpc=True, rpc_timeout=RPC_TIMEOUT_SECONDS)
    if not isinstance(result, str):
        return str(result)
    return result
