from typing import Annotated, Generator
from fastapi import Depends
from sqlmodel import Session
from services.dht11_service import DHT11Service
from db.database import engine
from repositories.dht11_repository import DHT11Repository
from repositories.user_repository import UserRepository
from services.auth_service import AuthService
from services.user_service import UserService


# --- Database session ---
def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session


DBSession = Annotated[Session, Depends(get_session)]


# --- Repository ---
def get_dht11_repository(session: DBSession) -> DHT11Repository:
    return DHT11Repository(session)


DHT11RepositoryDep = Annotated[DHT11Repository, Depends(get_dht11_repository)]


def get_user_repository(session: DBSession) -> UserRepository:
    return UserRepository(session)


UserRepositoryDep = Annotated[UserRepository, Depends(get_user_repository)]


# --- Service ---
def get_dht11_service(dht11_repo: DHT11RepositoryDep) -> DHT11Service:
    return DHT11Service(dht11_repo)


DHT11ServiceDep = Annotated[DHT11Service, Depends(get_dht11_service)]


def get_auth_service(user_repo: UserRepositoryDep) -> AuthService:
    return AuthService(user_repo)


AuthServiceDep = Annotated[AuthService, Depends(get_auth_service)]


def get_user_service(user_repo: UserRepositoryDep) -> UserService:
    return UserService(user_repo)


UserServiceDep = Annotated[UserService, Depends(get_user_service)]
