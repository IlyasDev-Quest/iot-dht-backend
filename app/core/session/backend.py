from uuid import UUID
from fastapi_sessions.backends.implementations import InMemoryBackend

from schemas.session import SessionData

session_backend = InMemoryBackend[UUID, SessionData]()
