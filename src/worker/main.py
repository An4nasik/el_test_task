import asyncio

from faststream import FastStream
from faststream.rabbit import RabbitRouter

from src.core.logging import setup_logging
from src.knowledge.loader import load_vectorstore
from src.worker.broker import broker
from src.worker.handlers import handle_audio, handle_text

router = RabbitRouter()


@router.subscriber("ai.text")
async def on_text(payload: dict) -> str:
    return await handle_text(payload)


@router.subscriber("ai.audio")
async def on_audio(payload: dict) -> str:
    return await handle_audio(payload)


broker.include_router(router)

app = FastStream(broker)


@app.on_startup
async def on_startup():
    setup_logging()
    # Run synchronous vectorstore loading in a thread to avoid blocking
    await asyncio.to_thread(load_vectorstore)


if __name__ == "__main__":
    app.run()
