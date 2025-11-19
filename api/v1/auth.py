from fastapi import APIRouter, Response
from core.session.backend import session_backend as backend
from schemas.credentials import Credentials
from dependencies import AuthServiceDep
from core.session.frontend import cookie

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/session")
async def create_session(
    auth_service: AuthServiceDep, Credentials: Credentials, response: Response
):
    session_id = await auth_service.authenticate(Credentials)
    if session_id is None:
        return Response(status_code=401)
    cookie.attach_to_response(response, session_id)
    return {"message": "Session created"}
