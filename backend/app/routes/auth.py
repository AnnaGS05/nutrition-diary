import uuid

from fastapi import APIRouter, Form, HTTPException, Request, Response
from passlib.context import CryptContext

from app.csrf import generate_csrf_token, set_csrf_cookie, CSRF_COOKIE_NAME
from app.database import get_connection
from app.logger import logger
from app.redis_client import redis_client

router = APIRouter(prefix="/auth", tags=["Auth"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)


@router.post("/register")
def register(username: str = Form(...), password: str = Form(...)):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        hashed = hash_password(password)
        cursor.execute(
            "INSERT INTO users (username, password) VALUES (%s, %s)",
            (username, hashed),
        )
        conn.commit()

        logger.info("user_registered", extra={"path": "/auth/register", "status_code": 201})

        return {"message": "User registered"}

    except Exception:
        conn.rollback()
        logger.error("user_registration_failed", extra={"path": "/auth/register", "status_code": 400})
        raise HTTPException(status_code=400, detail="User already exists")

    finally:
        cursor.close()
        conn.close()


@router.post("/login")
def login(response: Response, username: str = Form(...), password: str = Form(...)):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, password FROM users WHERE username = %s",
        (username,),
    )
    user = cursor.fetchone()

    cursor.close()
    conn.close()

    if not user or not verify_password(password, user[1]):
        logger.error("login_failed", extra={"path": "/auth/login", "status_code": 401})
        raise HTTPException(status_code=401, detail="Invalid username or password")

    session_id = str(uuid.uuid4())
    user_id = user[0]

    redis_client.set(session_id, user_id, ex=3600)

    response.set_cookie(
        key="session_id",
        value=session_id,
        httponly=True,
        max_age=3600,
        samesite="none" if settings.IS_PRODUCTION else "lax",,
        secure=False,
    )

    csrf_token = generate_csrf_token()
    set_csrf_cookie(response, csrf_token)

    logger.info("login_success", extra={"path": "/auth/login", "status_code": 200})

    return {
        "message": "Logged in",
        "csrf_token": csrf_token,
    }


@router.post("/logout")
def logout(request: Request, response: Response):
    session_id = request.cookies.get("session_id")

    if session_id:
        redis_client.delete(session_id)

    response.delete_cookie(
        key="session_id",
        samesite="none" if settings.IS_PRODUCTION else "lax",
        secure=settings.IS_PRODUCTION,
    )

    response.delete_cookie(
        key=CSRF_COOKIE_NAME,
        samesite="none" if settings.IS_PRODUCTION else "lax",
        secure=settings.IS_PRODUCTION,
    )

    logger.info("logout", extra={"path": "/auth/logout", "status_code": 200})

    return {"message": "Logged out"}


@router.get("/me")
def me(request: Request):
    session_id = request.cookies.get("session_id")

    if not session_id:
        return {"authenticated": False}

    user_id = redis_client.get(session_id)

    if not user_id:
        return {"authenticated": False}

    return {
        "authenticated": True,
        "user_id": int(user_id),
    }