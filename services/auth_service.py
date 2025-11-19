from uuid import uuid4, UUID

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

    async def _create_session(self, user: User) -> UUID:
        session_id = uuid4()
        data = SessionData(
            firstname=user.first_name,
            lastname=user.last_name,
            email=user.email,
            user_role=user.user_role,
        )
        await backend.create(session_id, data)

        return session_id
