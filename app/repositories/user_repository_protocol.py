from typing import Protocol

from models.user import User


class UserRepositoryProtocol(Protocol):
    def get_user_by_email(self, user_email: str) -> User | None:
        """Retrieve a user by their email."""
        ...

    def get_user_by_id(self, user_id: int) -> User | None:
        """Retrieve a user by their ID."""
        ...
