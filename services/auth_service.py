from uuid import uuid4, UUID

from enums.user_role import UserRole
from schemas.session import SessionData
from core.security import verify_password
from core.session.backend import session_backend as backend
from repositories.user_repository_protocol import UserRepositoryProtocol
from models.user import User
from schemas.credentials import Credentials


class AuthService:
    def __init__(self, user_repo: UserRepositoryProtocol):
        self.user_repo = user_repo

    async def authenticate(self, credentials: Credentials) -> UUID | None:
        user = self.user_repo.get_user_by_email(credentials.email)
        if not user or not verify_password(credentials.password, user.hashed_password):
            return None
        return await self._create_session(user)

    async def fake_authenticate(self) -> UUID:
        user = User(
            id=0,
            first_name="Fake",
            last_name="User",
            email="hello@gmail.com",
            user_role=UserRole.CEO,
            hashed_password="",
        )
        return await self._create_session(user)

    async def _create_session(self, user: User) -> UUID:
        if user.id is None:
            raise ValueError("Cannot create a session for a user without an ID")
        session_id = uuid4()
        data = SessionData(
            user_id=user.id,
            user_role=user.user_role,
        )
        await backend.create(session_id, data)

        return session_id
