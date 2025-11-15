from datetime import datetime
from sqlmodel import select, asc, desc
from core.db import DBSession
from models.dht11_models import DHT11Reading
from core.events import dispatch_event

class DHT11Service:
    @staticmethod
    def get_readings(start: datetime | None, end: datetime | None):
        if start and end and start > end:
            raise ValueError("Start date must be before end date")
        
        query = select(DHT11Reading)
        if start:
            query = query.where(DHT11Reading.timestamp >= start)
        if end:
            query = query.where(DHT11Reading.timestamp <= end)
        query = query.order_by(asc(DHT11Reading.timestamp))
        return query

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
