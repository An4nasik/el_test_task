from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.api.routes import router as api_router
from src.api.rpc import start_rpc, stop_rpc
from src.core.logging import setup_logging
from src.db.database import init_db
from src.knowledge.loader import load_vectorstore


@asynccontextmanager
def lifespan(app: FastAPI):
    setup_logging()
    load_vectorstore()
    await init_db()
    await start_rpc()
    yield
    await stop_rpc()


def create_app() -> FastAPI:
    app = FastAPI(title="AI Book Consultant", lifespan=lifespan)
    app.include_router(api_router)
    return app


app = create_app()
