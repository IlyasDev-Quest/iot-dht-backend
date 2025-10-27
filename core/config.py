import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "IoT DHT Project"
    environment: str = os.getenv("ENV", "dev")
    database_url: str = os.getenv("DATABASE_URL", f"sqlite:///./database.db")

    class Config:
        env_file = ".env"


settings = Settings()
