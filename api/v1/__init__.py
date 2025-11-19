from fastapi import APIRouter
from .dht11 import router as dht11_router
from .events import router as events_router
from .auth import router as auth_router

router = APIRouter(prefix="/v1")
router.include_router(dht11_router)
router.include_router(events_router)
router.include_router(auth_router)
