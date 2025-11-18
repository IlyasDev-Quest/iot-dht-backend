from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    app_name: str = "IoT DHT Project"
    environment: str = "dev"
    database_url: str = "sqlite:///./database.db"
    cors_origins: List[str] = ["http://localhost:3000"]
    secret_key: str = "super-secret-key"

    class Config:
        env_file = ".env"

settings = Settings()
