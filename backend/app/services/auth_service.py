from fastapi import Request, HTTPException
from app.redis_client import redis_client


def get_current_user_id(request: Request):
    session_id = request.cookies.get("session_id")

    if not session_id:
        raise HTTPException(status_code=401, detail="Unauthorized")

    user_id = redis_client.get(session_id)

    if not user_id:
        raise HTTPException(status_code=401, detail="Unauthorized")

    return int(user_id)