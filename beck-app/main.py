import logging
import subprocess
from contextlib import asynccontextmanager

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api import router as api_router, router
import uvicorn
from core.config import settings
from core.models import create_tables_method
from api.routers import router
from core.db_helper import db_helper

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Application started")
    #await create_tables_method.create_tables()


    yield


main_app = FastAPI(
    lifespan=lifespan,
)
origins = [

    "http://localhost:5173",
    "https://localhost:5173",
    "http://localhost:3000",
    "https://localhost:3000",
]

# Добавляем CORS middleware
main_app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

main_app.include_router(api_router, prefix=settings.api.prefix)

main_app.include_router(router.router, prefix=settings.api.prefix)

if __name__ == '__main__':
    uvicorn.run('main:main_app',
                host=settings.run.host,
                port=settings.run.port,
                reload=True,
                )
