from typing import Literal
from fastapi import APIRouter, HTTPException, Query
from fastapi_pagination.limit_offset import LimitOffsetPage
from fastapi_pagination.ext.sqlmodel import paginate
from datetime import datetime
from core.db import DBSession
from schemas.dht11_schemas import DHT11ChartData, DHT11ReadingData
from models.dht11_models import DHT11Reading
from services.dht11_service import DHT11Service

router = APIRouter(prefix="/dht11", tags=["dht11"])

@router.get("/readings", response_model=LimitOffsetPage[DHT11Reading])
def get_readings(session: DBSession,
                 start_date: datetime | None = Query(None),
                 end_date: datetime | None = Query(None)):
    try:
        query = DHT11Service.get_readings(start_date, end_date)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    return paginate(session, query)

# routes/dht11_routes.py
@router.get("/readings/chart", response_model=list[DHT11ChartData])
def get_readings_chart(
    session: DBSession,
    start_date: datetime = Query(
        ...,
        description="Start date for chart data (inclusive)",
        example="2025-01-01T00:00:00Z"
    ),
    end_date: datetime = Query(
        ...,
        description="End date for chart data (inclusive)",
        example="2025-01-31T23:59:59Z"
    ),
    group_by: Literal["minute", "hour", "day", "week", "month"] = Query(
        "day",
        description="Time interval for data aggregation"
    )
):
    try:
        return DHT11Service.get_aggregated_readings(session, start_date, end_date, group_by)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))

@router.post("/readings", response_model=DHT11Reading, status_code=201)
def create_reading(session: DBSession, reading_data: DHT11ReadingData):
    return DHT11Service.create_reading(session, reading_data.temperature, reading_data.humidity)

@router.get("/readings/latest", response_model=DHT11Reading)
def get_latest_reading(session: DBSession):
    result = DHT11Service.get_latest_reading(session)
    if not result:
        raise HTTPException(status_code=404, detail="No readings found")
    return result