from fastapi import APIRouter
from datetime import datetime

router = APIRouter(
    prefix="/dht11",
    tags=["dht11"]
)

@router.get("/test")
async def get_test():
    return {
        "status": "DHT11 sensor test is operational",
        "timestamp": datetime.now()
    }