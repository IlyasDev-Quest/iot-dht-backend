from typing import Literal
from fastapi import APIRouter, HTTPException, Query
from fastapi_pagination import LimitOffsetPage
from datetime import datetime
from dependencies import DHT11ServiceDep
from schemas.dht11 import DHT11ChartData, DHT11ReadingData
from models.dht11_models import DHT11Reading

router = APIRouter(prefix="/dht11", tags=["dht11"])

@router.get("/readings", response_model=LimitOffsetPage[DHT11Reading])
def get_readings(
    service: DHT11ServiceDep, 
    start_date: datetime | None = Query(None),
    end_date: datetime | None = Query(None),
):
    """Get paginated list of DHT11 readings with optional date filtering."""
    try:
        return service.get_readings(start_date, end_date)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))


@router.get("/readings/chart", response_model=list[DHT11ChartData])
def get_readings_chart(
    service: DHT11ServiceDep,
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
    ),
):
    """Get aggregated DHT11 readings for charting."""
    try:
        return service.get_aggregated_readings(start_date, end_date, group_by)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))


@router.post("/readings", response_model=DHT11Reading, status_code=201)
def create_reading(
    service: DHT11ServiceDep,
    reading_data: DHT11ReadingData,
):
    """Create a new DHT11 sensor reading."""
    return service.create_reading(reading_data)


@router.get("/readings/latest", response_model=DHT11Reading)
def get_latest_reading(service: DHT11ServiceDep):
    """Get the most recent DHT11 reading."""
    result = service.get_latest_reading()
    if not result:
        raise HTTPException(status_code=404, detail="No readings found")
    return result