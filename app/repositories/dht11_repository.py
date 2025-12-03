from datetime import datetime
from typing import Any
from fastapi_pagination import LimitOffsetPage
from fastapi_pagination.ext.sqlmodel import paginate
from sqlmodel import String, cast, func, select, asc, desc, Session
from models.dht11 import DHT11Reading
from schemas.dht11 import DHT11ReadingData


class DHT11Repository:
    def __init__(self, session: Session):
        self.session = session

    def get_readings(
        self,
        start_date: datetime | None,
        end_date: datetime | None,
    ) -> LimitOffsetPage[DHT11Reading]:

        query = select(DHT11Reading)
        if start_date:
            query = query.where(DHT11Reading.timestamp >= start_date)
        if end_date:
            query = query.where(DHT11Reading.timestamp <= end_date)

        query = query.order_by(asc(DHT11Reading.timestamp))

        return paginate(self.session, query)

    def get_aggregated_readings(
        self, start_date: datetime, end_date: datetime, time_format: str
    ) -> list[Any]:
        """Execute aggregation query and return aggregated database results."""

        # PostgreSQL uses to_char for timestamp formatting
        time_bucket = cast(
            func.to_char(DHT11Reading.timestamp, time_format), String
        ).label("time_bucket")

        avg_temp = func.avg(DHT11Reading.temperature).label("avg_temperature")
        avg_hum = func.avg(DHT11Reading.humidity).label("avg_humidity")
        min_temp = func.min(DHT11Reading.temperature).label("min_temperature")
        max_temp = func.max(DHT11Reading.temperature).label("max_temperature")
        min_hum = func.min(DHT11Reading.humidity).label("min_humidity")
        max_hum = func.max(DHT11Reading.humidity).label("max_humidity")
        count_readings = func.count().label("reading_count")

        stmt = (
            select(  # type: ignore[call-overload]
                time_bucket,
                avg_temp,
                avg_hum,
                min_temp,
                max_temp,
                min_hum,
                max_hum,
                count_readings,
            )
            .where(
                DHT11Reading.timestamp >= start_date, DHT11Reading.timestamp <= end_date
            )
            .group_by(time_bucket)
            .order_by(time_bucket)
        )

        results = self.session.exec(stmt).all()
        return results

    def create_reading(self, dht11_reading_data: DHT11ReadingData) -> DHT11Reading:
        """Create and persist a new DHT11 reading."""
        reading = DHT11Reading(
            temperature=dht11_reading_data.temperature,
            humidity=dht11_reading_data.humidity,
        )
        self.session.add(reading)
        self.session.commit()
        self.session.refresh(reading)
        return reading

    def get_latest_reading(self) -> DHT11Reading | None:
        """Get the most recent reading."""
        query = select(DHT11Reading).order_by(desc(DHT11Reading.timestamp)).limit(1)
        return self.session.exec(query).first()
