from sqlmodel import SQLModel, Field
from datetime import datetime

class DHT11ReadingData(SQLModel):
    temperature: float = Field(..., description="Temperature in Celsius")
    humidity: float = Field(..., description="Relative humidity in %")

class DHT11ChartData(SQLModel):
    timestamp: datetime = Field(..., description="Timestamp of the aggregated period")
    avg_temperature: float = Field(..., description="Average temperature in Celsius")
    avg_humidity: float = Field(..., description="Average relative humidity in %")
    min_temperature: float | None = Field(None, description="Minimum temperature in Celsius")
    max_temperature: float | None = Field(None, description="Maximum temperature in Celsius")
    min_humidity: float | None = Field(None, description="Minimum relative humidity in %")
    max_humidity: float | None = Field(None, description="Maximum relative humidity in %")
    reading_count: int = Field(..., description="Number of readings aggregated")