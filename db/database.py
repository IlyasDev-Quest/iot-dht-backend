from sqlmodel import SQLModel, create_engine
from core.config import settings

connect_args = {"check_same_thread": False} if "sqlite" in settings.database_url else {}
engine = create_engine(settings.database_url, connect_args=connect_args)


async def create_db_and_tables():
    print(f"Creating database tables in {settings.environment} environment...")
    SQLModel.metadata.create_all(engine)
    print("Database and tables created.")


async def close_db_connection():
    print("Closing database connections...")
    engine.dispose()
    print("Database connections closed.")
