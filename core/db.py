# app/core/db.py
from fastapi import Depends
from sqlmodel import SQLModel, Session, create_engine
from typing import Annotated, Generator
from .config import settings

connect_args = {"check_same_thread": False} if "sqlite" in settings.database_url else {}
engine = create_engine(settings.database_url, connect_args=connect_args)


async def create_db_and_tables():
    print(f"Creating database tables in {settings.environment} environment...")
    SQLModel.metadata.create_all(engine)
    print("Database and tables created.")


def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session

DBSession = Annotated[Session, Depends(get_session)]