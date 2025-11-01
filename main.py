from fastapi import FastAPI
from contextlib import asynccontextmanager

from fastapi_pagination import add_pagination
from api.v1 import router as v1_router
from core.db import create_db_and_tables

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup code
    await create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(v1_router, prefix="/api")

add_pagination(app)