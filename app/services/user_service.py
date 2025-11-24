from schemas.user import UserSchema
from repositories.user_repository_protocol import UserRepositoryProtocol


class UserService:
    def __init__(self, user_repo: UserRepositoryProtocol):
        self.user_repo = user_repo

    async def get_user_by_id(self, user_id: int) -> UserSchema | None:
        user = self.user_repo.get_user_by_id(user_id)
        if user is None:
            return None
        return UserSchema.model_validate(user)
