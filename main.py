from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.config.redis import init_redis, close_redis
from app.route.auth import router as auth_router
from app.route.task import router as task_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_redis()

    yield

    await close_redis()
    # Perform any cleanup tasks here

app=FastAPI(
    title="Task Manager Api with Fast Api",
    description="Highly Engineered Fast Api Backend for a Task Manager Application",
    lifespan=lifespan,
)


app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(task_router, prefix="/task", tags=["Task"])