from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from schemas.user import UserSchema
from dependencies import UserServiceDep
from schemas.session import SessionData
from core.session.verifier import verifier
from core.session.backend import session_backend
from core.session.frontend import cookie

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", dependencies=[Depends(cookie)], response_model=UserSchema)
async def get_current_user(
    session_data: Annotated[SessionData, Depends(verifier)],
    user_service: UserServiceDep,
) -> UserSchema:
    user = await user_service.get_user_by_id(session_data.user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user
