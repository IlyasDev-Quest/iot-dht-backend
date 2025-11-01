from fastapi import APIRouter, Query
from datetime import datetime

from fastapi_pagination.limit_offset import LimitOffsetPage
from fastapi_pagination.ext.sqlmodel import paginate
from sqlmodel import asc, select
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

@router.get("/readings", response_model=LimitOffsetPage[DHT11Reading])
def get_readings(
    session: DBSession,
    start: datetime | None = Query(None, description="Start timestamp"),
    end: datetime | None = Query(None, description="End timestamp")
):
    query = select(DHT11Reading)

    if start is not None:
        query = query.where(DHT11Reading.timestamp >= start)
    if end is not None:
        query = query.where(DHT11Reading.timestamp <= end)

    query = query.order_by(asc(DHT11Reading.timestamp))
    
    return paginate(session, query)