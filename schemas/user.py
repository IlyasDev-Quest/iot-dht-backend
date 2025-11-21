from pydantic import BaseModel, EmailStr
from enums.user_role import UserRole


class UserBase(BaseModel):
    first_name: str | None
    last_name: str | None
    email: EmailStr
    user_role: UserRole


class UserSchema(UserBase):
    id: int

    model_config = {"from_attributes": True}
