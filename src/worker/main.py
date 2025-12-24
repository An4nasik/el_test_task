from faststream import FastStream
from faststream.rabbit import RabbitRouter

from src.worker.broker import broker
from src.worker.handlers import handle_audio, handle_text

router = RabbitRouter()


@router.subscriber("ai.text", rpc=True)
async def on_text(payload):
    return await handle_text(payload, None, None)


@router.subscriber("ai.audio", rpc=True)
async def on_audio(payload):
    return await handle_audio(payload, None, None)


app = FastStream(broker, router)


if __name__ == "__main__":
    app.run()
