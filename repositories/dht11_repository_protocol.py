
from datetime import datetime
from typing import Protocol, Any
from models.dht11_models import DHT11Reading
from schemas.dht11 import DHT11ReadingData


class DHT11RepositoryProtocol(Protocol):
    """Protocol defining the interface for DHT11 repository implementations."""
    
    def get_readings_query(
        self, 
        start_date: datetime | None = None, 
        end_date: datetime | None = None
    ) -> Any:
        """Returns a query for readings with optional date filters."""
        ...
    
    def get_aggregated_readings(
        self,
        start_date: datetime,
        end_date: datetime,
        time_format: str
    ) -> list[Any]:
        """Execute aggregation query and return raw database results."""
        ...
    
    def create_reading(self, dht11_reading_data: DHT11ReadingData) -> DHT11Reading:
        """Create and persist a new DHT11 reading."""
        ...
    
    def get_latest_reading(self) -> DHT11Reading | None:
        """Get the most recent reading."""
        ...
