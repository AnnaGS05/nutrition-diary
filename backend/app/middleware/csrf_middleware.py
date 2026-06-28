from fastapi import Request, HTTPException
from app.csrf import verify_csrf


class CSRFMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            return await self.app(scope, receive, send)

        request = Request(scope, receive=receive)

        if request.method in ("POST", "PUT", "PATCH", "DELETE"):
            verify_csrf(request)

        return await self.app(scope, receive, send)