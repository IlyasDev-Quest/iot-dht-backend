from fastapi import FastAPI

from fastapi_pagination import add_pagination
from api.v1 import router as v1_router
from core.config import settings

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.include_router(v1_router, prefix="/api")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

add_pagination(app)
