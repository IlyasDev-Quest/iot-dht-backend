from datetime import datetime
from typing import Literal
from sqlmodel import Session
from fastapi_pagination.limit_offset import LimitOffsetPage
from fastapi_pagination.ext.sqlmodel import paginate
from repositories.dht11_repository_protocol import DHT11RepositoryProtocol
from schemas.dht11 import DHT11ChartData, DHT11ReadingData
from models.dht11_models import DHT11Reading
from core.events import dispatch_event

class DHT11Service:
    def __init__(self, repository: DHT11RepositoryProtocol):
        self.repository = repository
    
    def get_readings(
        self,
        start_date: datetime | None = None,
        end_date: datetime | None = None,
        limit: int = 50,
        offset: int = 0
    ):
        if start_date and end_date and start_date > end_date:
            raise ValueError("start_date must be before end_date")

        return self.repository.get_readings(start_date, end_date)
    
    def get_aggregated_readings(
        self,
        start_date: datetime,
        end_date: datetime,
        group_by: Literal["minute", "hour", "day", "week", "month"]
    ) -> list[DHT11ChartData]:
        """Get aggregated readings for charting."""
        if start_date > end_date:
            raise ValueError("start_date must be before end_date")
        
        # Define time bucket based on group_by
        time_format = {
            "minute": "%Y-%m-%d %H:%M:00",
            "hour": "%Y-%m-%d %H:00:00",
            "day": "%Y-%m-%d",
            "week": "%Y-%W",
            "month": "%Y-%m"
        }[group_by]
        
        results = self.repository.get_aggregated_readings(
            start_date, 
            end_date, 
            time_format
        )
        
        return [
            DHT11ChartData(
                timestamp=datetime.fromisoformat(r.time_bucket),
                avg_temperature=round(r.avg_temperature, 2),
                avg_humidity=round(r.avg_humidity, 2),
                min_temperature=round(r.min_temperature, 2) if r.min_temperature else None,
                max_temperature=round(r.max_temperature, 2) if r.max_temperature else None,
                min_humidity=round(r.min_humidity, 2) if r.min_humidity else None,
                max_humidity=round(r.max_humidity, 2) if r.max_humidity else None,
                reading_count=r.reading_count
            )
            for r in results
        ]
    
    def create_reading(self, reading_data: DHT11ReadingData) -> DHT11Reading:
        """Create a new DHT11 reading."""
        reading = self.repository.create_reading(reading_data)
        dispatch_event("dht11_reading_created")
        return reading
    
    def get_latest_reading(self) -> DHT11Reading | None:
        """Get the most recent reading."""
        return self.repository.get_latest_reading()