from fastapi_sessions.frontends.implementations import SessionCookie, CookieParameters
from core.config import settings

cookie_params = CookieParameters()

# Uses UUID
cookie = SessionCookie(
    cookie_name="cookie",
    identifier="general_verifier",
    auto_error=True,
    secret_key=settings.secret_key,
    cookie_params=cookie_params,
)
