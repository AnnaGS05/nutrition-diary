from fastapi import Request
from app.csrf import verify_csrf

CSRF_EXEMPT_PATHS = ["/auth/login", "/auth/register"]


class CSRFMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            return await self.app(scope, receive, send)

        request = Request(scope, receive=receive)

        if request.method in ("POST", "PUT", "PATCH", "DELETE"):
            if request.url.path not in CSRF_EXEMPT_PATHS:
                verify_csrf(request)

        return await self.app(scope, receive, send)