from uuid import UUID
from fastapi import APIRouter, Depends, Response
from schemas.credentials import Credentials
from dependencies import AuthServiceDep
from core.session.frontend import cookie

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/session", status_code=201)
async def create_session(
    response: Response,
    auth_service: AuthServiceDep,
    credentials: Credentials,
):
    session_id = await auth_service.authenticate(credentials)
    if session_id is None:
        return Response(status_code=401)
    cookie.attach_to_response(response, session_id)


@router.delete("/session", status_code=204)
async def delete_session(
    response: Response,
    auth_service: AuthServiceDep,
    session_id: UUID = Depends(cookie),
):
    await auth_service.terminate_session(session_id)
    cookie.delete_from_response(response)
