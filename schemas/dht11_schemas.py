from sqlmodel import SQLModel, Field
from datetime import datetime

class DHT11ReadingData(SQLModel):
    temperature: float = Field(..., description="Temperature in Celsius")
    humidity: float = Field(..., description="Relative humidity in %")
