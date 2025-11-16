from datetime import datetime
from sqlmodel import func, select, asc, desc, text
from schemas.dht11_schemas import DHT11ChartData
from core.db import DBSession
from models.dht11_models import DHT11Reading
from core.events import dispatch_event

class DHT11Service:
    @staticmethod
    def get_readings(start_date: datetime | None, end_date: datetime | None):
        if start_date and end_date and start_date > end_date:
            raise ValueError("start_date date must be before end_date date")
        
        query = select(DHT11Reading)
        if start_date:
            query = query.where(DHT11Reading.timestamp >= start_date)
        if end_date:
            query = query.where(DHT11Reading.timestamp <= end_date)
        query = query.order_by(asc(DHT11Reading.timestamp))
        return query
    
    @staticmethod
    def get_aggregated_readings(
        session, 
        start_date: datetime, 
        end_date: datetime, 
        group_by: str
    ) -> list[DHT11ChartData]:
        # Define time bucket based on group_by
        time_format = {
            "minute": "%Y-%m-%d %H:%M:00",
            "hour": "%Y-%m-%d %H:00:00",
            "day": "%Y-%m-%d",
            "week": "%Y-%W",
            "month": "%Y-%m"
        }[group_by]
        
        # Use raw SQL for aggregation with text()
        raw_query = text(f"""
        SELECT 
            strftime('{time_format}', timestamp) as time_bucket,
            AVG(temperature) as avg_temperature,
            AVG(humidity) as avg_humidity,
            MIN(temperature) as min_temperature,
            MAX(temperature) as max_temperature,
            MIN(humidity) as min_humidity,
            MAX(humidity) as max_humidity,
            COUNT(*) as reading_count
        FROM dht11reading
        WHERE timestamp >= :start_date AND timestamp <= :end_date
        GROUP BY time_bucket
        ORDER BY time_bucket
        """)
        
        results = session.exec(
            raw_query,
            params={"start_date": start_date, "end_date": end_date}
        ).all()
        
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

    @staticmethod
    def create_reading(session: DBSession, temperature: float, humidity: float) -> DHT11Reading:
        reading = DHT11Reading(temperature=temperature, humidity=humidity)
        session.add(reading)
        session.commit()
        session.refresh(reading)
        dispatch_event("dht11_reading_created")
        return reading

    @staticmethod
    def get_latest_reading(session: DBSession) -> DHT11Reading | None:
        query = select(DHT11Reading).order_by(desc(DHT11Reading.timestamp)).limit(1)
        return session.exec(query).first()
