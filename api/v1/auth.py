from fastapi import APIRouter, Response
from uuid import uuid4
from core.session.backend import session_backend as backend
from schemas.session import SessionData
from schemas.credentials import Credentials

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/session")
async def create_session(Credentials: Credentials):
    return {}