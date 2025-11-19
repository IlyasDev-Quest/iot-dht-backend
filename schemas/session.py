from pydantic import BaseModel, Field
from enums.user_role import UserRole


class SessionData(BaseModel):
    firstname: str = Field(...)
    lastname: str = Field(...)
    email: str = Field(...)
    user_role: UserRole = Field(...)
