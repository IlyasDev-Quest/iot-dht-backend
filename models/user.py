from sqlmodel import SQLModel, Field
from typing import Optional
from enums.user_role import UserRole


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    first_name: str = Field(index=True)
    last_name: str = Field(index=True)
    email: str = Field(index=True, unique=True)
    hashed_password: str
    user_role: UserRole
