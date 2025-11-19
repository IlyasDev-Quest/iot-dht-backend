from sqlmodel import Session, select
from typing import Optional
from models.user import User
from repositories.user_repository_protocol import UserRepositoryProtocol


class UserRepository(UserRepositoryProtocol):
    def __init__(self, session: Session):
        self.session = session

    def get_user_by_email(self, user_email: str) -> User | None:
        """
        Retrieve a user by their email.
        Returns None if no user is found.
        """
        statement = select(User).where(User.email == user_email)
        user = self.session.exec(statement).first()
        return user
