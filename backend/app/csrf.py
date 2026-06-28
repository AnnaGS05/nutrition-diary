import secrets
from fastapi import HTTPException, Request, Response
from app.config import settings

CSRF_COOKIE_NAME = "csrf_token"
CSRF_HEADER_NAME = "X-CSRF-Token"


def generate_csrf_token() -> str:
    return secrets.token_urlsafe(32)


def set_csrf_cookie(response: Response, token: str):
    response.set_cookie(
        key=CSRF_COOKIE_NAME,
        value=token,
        httponly=False,
        secure=settings.IS_PRODUCTION,
        samesite="none" if settings.IS_PRODUCTION else "lax",
        max_age=3600
    )


def verify_csrf(request: Request):
    if request.method in ("GET", "HEAD", "OPTIONS"):
        return

    cookie_token = request.cookies.get(CSRF_COOKIE_NAME)
    header_token = request.headers.get(CSRF_HEADER_NAME)

    if not cookie_token or not header_token:
        raise HTTPException(status_code=403, detail="CSRF token missing")

    if cookie_token != header_token:
        raise HTTPException(status_code=403, detail="Invalid CSRF token")