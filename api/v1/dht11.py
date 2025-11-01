from typing import Annotated, Sequence
from fastapi import APIRouter, Query
from datetime import datetime

from sqlmodel import select
from models.dht11_models import DHT11Reading
from core.db import DBSession

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

@router.get("/")
async def get_all(
    session: DBSession,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
) -> Sequence[DHT11Reading]:
    readings = session.exec(
        select(DHT11Reading).offset(offset).limit(limit)
    ).all()
    return readings
    