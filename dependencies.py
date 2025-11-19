from typing import Annotated, Generator

from fastapi import Depends
from sqlmodel import Session
from services.dht11_service import DHT11Service
from db.database import engine

from repositories.dht11_repository import DHT11Repository

def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session

DBSession = Annotated[Session, Depends(get_session)]

def get_dht11_repository(session: DBSession) -> DHT11Repository:
    return DHT11Repository(session)

DHT11RepositoryDep = Annotated[DHT11Repository, Depends(get_dht11_repository)]

def get_dht11_service(repository: DHT11RepositoryDep) -> DHT11Service:
    return DHT11Service(repository)

DHT11ServiceDep = Annotated[DHT11Service, Depends(get_dht11_service)]