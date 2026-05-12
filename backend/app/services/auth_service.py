from fastapi import Request
from app.redis_client import redis_client


def get_current_user_id(request: Request):
    session_id = request.cookies.get("session_id")

    if not session_id:
        return None

    user_id = redis_client.get(session_id)

    if not user_id:
        return None

    return int(user_id)