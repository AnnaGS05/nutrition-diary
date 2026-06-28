from fastapi import HTTPException, Request

from app.csrf import verify_csrf
from app.redis_client import redis_client


def get_current_user_id(request: Request):
    if request.method in ("POST", "PUT", "PATCH", "DELETE"):
        verify_csrf(request)

    session_id = request.cookies.get("session_id")

    if not session_id:
        raise HTTPException(status_code=401, detail="Unauthorized")

    user_id = redis_client.get(session_id)

    if not user_id:
        raise HTTPException(status_code=401, detail="Unauthorized")

    return int(user_id)