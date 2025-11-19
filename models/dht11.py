from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional


class DHT11Reading(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    temperature: float = Field(..., description="Temperature in Celsius")
    humidity: float = Field(..., description="Relative humidity in %")
    timestamp: datetime = Field(
        default_factory=datetime.now, description="Time of reading", index=True
    )
