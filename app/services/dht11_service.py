from datetime import datetime
from typing import Literal
from repositories.dht11_repository_protocol import DHT11RepositoryProtocol
from schemas.dht11 import DHT11ChartData, DHT11ReadingData
from models.dht11 import DHT11Reading
from core.events import dispatch_event


class DHT11Service:
    def __init__(self, dht11_repo: DHT11RepositoryProtocol):
        self.dht11_repo = dht11_repo

    def get_readings(
        self,
        start_date: datetime | None = None,
        end_date: datetime | None = None,
        limit: int = 50,
        offset: int = 0,
    ):
        if start_date and end_date and start_date > end_date:
            raise ValueError("start_date must be before end_date")

        return self.dht11_repo.get_readings(start_date, end_date)

    def get_aggregated_readings(
        self,
        start_date: datetime,
        end_date: datetime,
        group_by: Literal["minute", "hour", "day", "week", "month"],
    ) -> list[DHT11ChartData]:
        """Get aggregated readings for charting."""
        if start_date > end_date:
            raise ValueError("start_date must be before end_date")

        # Define time bucket based on group_by (PostgreSQL format)
        time_format = {
            "minute": "YYYY-MM-DD HH24:MI:00",
            "hour": "YYYY-MM-DD HH24:00:00",
            "day": "YYYY-MM-DD",
            "week": "IYYY-IW",  # ISO year and ISO week
            "month": "YYYY-MM",
        }[group_by]

        results = self.dht11_repo.get_aggregated_readings(
            start_date, end_date, time_format
        )

        return [
            DHT11ChartData(
                timestamp=self._parse_time_bucket(r.time_bucket, group_by),
                avg_temperature=round(r.avg_temperature, 2),
                avg_humidity=round(r.avg_humidity, 2),
                min_temperature=(
                    round(r.min_temperature, 2) if r.min_temperature else None
                ),
                max_temperature=(
                    round(r.max_temperature, 2) if r.max_temperature else None
                ),
                min_humidity=round(r.min_humidity, 2) if r.min_humidity else None,
                max_humidity=round(r.max_humidity, 2) if r.max_humidity else None,
                reading_count=r.reading_count,
            )
            for r in results
        ]

    def _parse_time_bucket(self, time_bucket: str, group_by: str) -> datetime:
        """Parse time bucket string back to datetime based on grouping."""
        if group_by == "minute":
            return datetime.strptime(time_bucket, "%Y-%m-%d %H:%M:%S")
        elif group_by == "hour":
            return datetime.strptime(time_bucket, "%Y-%m-%d %H:%M:%S")
        elif group_by == "day":
            return datetime.strptime(time_bucket, "%Y-%m-%d")
        elif group_by == "week":
            # PostgreSQL ISO week format: "2025-47"
            year, week = time_bucket.split("-")
            # Get first day of the ISO week
            return datetime.strptime(f"{year}-W{week}-1", "%G-W%V-%u")
        elif group_by == "month":
            return datetime.strptime(time_bucket + "-01", "%Y-%m-%d")
        else:
            raise ValueError(f"Unknown group_by: {group_by}")

    def create_reading(self, reading_data: DHT11ReadingData) -> DHT11Reading:
        """Create a new DHT11 reading."""
        reading = self.dht11_repo.create_reading(reading_data)
        dispatch_event("dht11_reading_created")
        return reading

    def get_latest_reading(self) -> DHT11Reading | None:
        """Get the most recent reading."""
        return self.dht11_repo.get_latest_reading()
