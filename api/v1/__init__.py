from fastapi import APIRouter
from .dht11 import router as dht11_router

router = APIRouter(prefix="/v1")
router.include_router(dht11_router)
