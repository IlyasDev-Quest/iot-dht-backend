from fastapi import APIRouter, HTTPException, Query
from datetime import datetime

from fastapi_pagination.limit_offset import LimitOffsetPage
from fastapi_pagination.ext.sqlmodel import paginate
from sqlmodel import asc, desc, select
from schemas.dht11_schemas import DHT11ReadingData
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
    end: datetime | None = Query(None, description="End timestamp"),
) -> LimitOffsetPage[DHT11Reading]:
    
    query = select(DHT11Reading)

    if start and end and start > end:
        raise HTTPException(status_code=422, detail="Start date must be before end date")
    
    if start is not None:
        query = query.where(DHT11Reading.timestamp >= start)
    if end is not None:
        query = query.where(DHT11Reading.timestamp <= end)

    query = query.order_by(asc(DHT11Reading.timestamp))
    
    return paginate(session, query)

@router.post("/readings", response_model=DHT11Reading, status_code=201)
def create_reading(
    session: DBSession,
    reading_data: DHT11ReadingData,
) -> DHT11Reading:

    new_reading = DHT11Reading(
        temperature=reading_data.temperature,
        humidity=reading_data.humidity,
    )

    session.add(new_reading)
    session.commit()
    session.refresh(new_reading)

    return new_reading

@router.get("/readings/latest", response_model=DHT11Reading)
def get_latest_reading(
    session: DBSession,
) -> DHT11Reading:

    query = select(DHT11Reading).order_by(desc(DHT11Reading.timestamp)).limit(1)
    result = session.exec(query).first()

    if result is None:
        raise HTTPException(status_code=404, detail="No readings found")

    return result