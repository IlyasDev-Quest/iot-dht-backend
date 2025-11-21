from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    app_name: str = "IoT DHT Project"
    environment: str = "dev"
    cors_origins: List[str] = ["http://localhost:3000"]
    database_url: str
    secret_key: str 


settings = Settings() # type: ignore
