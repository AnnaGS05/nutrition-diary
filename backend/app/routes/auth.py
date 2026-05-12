import uuid

from fastapi import APIRouter, Form, Request, Response

from app.database import get_connection
from app.logger import logger
from app.redis_client import redis_client

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register")
def register(username: str = Form(...), password: str = Form(...)):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO users (username, password) VALUES (%s, %s)",
            (username, password)
        )
        conn.commit()

        logger.info(
            "user_registered",
            extra={
                "path": "/auth/register",
                "status_code": 201
            }
        )

        return {"message": "User registered"}

    except Exception:
        conn.rollback()

        logger.error(
            "user_registration_failed",
            extra={
                "path": "/auth/register",
                "status_code": 400
            }
        )

        return {"error": "User already exists"}

    finally:
        cursor.close()
        conn.close()


@router.post("/login")
def login(response: Response, username: str = Form(...), password: str = Form(...)):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id FROM users WHERE username = %s AND password = %s",
        (username, password)
    )

    user = cursor.fetchone()

    cursor.close()
    conn.close()

    if not user:
        logger.error(
            "login_failed",
            extra={
                "path": "/auth/login",
                "status_code": 401
            }
        )

        return {"error": "Invalid username or password"}

    session_id = str(uuid.uuid4())
    user_id = user[0]

    redis_client.set(session_id, user_id, ex=3600)

    response.set_cookie(
        key="session_id",
        value=session_id,
        httponly=True,
        max_age=3600
    )

    logger.info(
        "login_success",
        extra={
            "path": "/auth/login",
            "status_code": 200
        }
    )

    return {"message": "Logged in"}


@router.post("/logout")
def logout(request: Request, response: Response):
    session_id = request.cookies.get("session_id")

    if session_id:
        redis_client.delete(session_id)

    response.delete_cookie("session_id")

    logger.info(
        "logout",
        extra={
            "path": "/auth/logout",
            "status_code": 200
        }
    )

    return {"message": "Logged out"}


@router.get("/me")
def me(request: Request):
    session_id = request.cookies.get("session_id")

    if not session_id:
        logger.info(
            "auth_check_failed",
            extra={
                "path": "/auth/me",
                "status_code": 401
            }
        )

        return {"authenticated": False}

    user_id = redis_client.get(session_id)

    if not user_id:
        logger.info(
            "auth_check_failed",
            extra={
                "path": "/auth/me",
                "status_code": 401
            }
        )

        return {"authenticated": False}

    logger.info(
        "auth_check_success",
        extra={
            "path": "/auth/me",
            "status_code": 200
        }
    )

    return {
        "authenticated": True,
        "user_id": user_id
    }