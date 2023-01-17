from fastapi import FastAPI
from src.common.db.connect import init_pool
from src.common.core.redis_config import redis_config

APP = FastAPI(
    title="TASK API",
    version="1.0.0",
    description="Task Swagger",
)


@APP.on_event("startup")
async def startup():
    rd = redis_config()
    rd.delete()
    await init_pool()
