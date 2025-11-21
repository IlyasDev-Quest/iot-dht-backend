from fastapi import APIRouter, Response
from schemas.credentials import Credentials
from dependencies import AuthServiceDep
from core.session.frontend import cookie

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/session", status_code=201)
async def create_session(
    auth_service: AuthServiceDep, credentials: Credentials, response: Response
):
    session_id = await auth_service.authenticate(credentials)
    if session_id is None:
        return Response(status_code=401)
    cookie.attach_to_response(response, session_id)
