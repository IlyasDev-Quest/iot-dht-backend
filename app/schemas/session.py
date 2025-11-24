from pydantic import BaseModel, Field
from enums.user_role import UserRole


class SessionData(BaseModel):
    user_id: int = Field(...)
    user_role: UserRole = Field(...)
