from fastapi import FastAPI
from contextlib import asynccontextmanager

from fastapi_pagination import add_pagination
from api.v1 import router as v1_router
from core.db import close_db_connection, create_db_and_tables
from core.config import settings

from fastapi.middleware.cors import CORSMiddleware

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup code
    await create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(v1_router, prefix="/api")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

add_pagination(app)