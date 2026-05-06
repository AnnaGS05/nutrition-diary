import socket

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.config import settings
from app.middleware import RequestLoggingMiddleware
from app.routes.auth import router as auth_router
from app.routes.entries import router as entries_router

app = FastAPI(title=settings.APP_NAME)

app.add_middleware(RequestLoggingMiddleware)

app.mount("/static", StaticFiles(directory="app/static"), name="static")

templates = Jinja2Templates(directory="app/templates")

app.include_router(entries_router)
app.include_router(auth_router)


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html"
    )


@app.get("/health")
def health():
    return {
        "status": "ok",
        "environment": settings.ENVIRONMENT,
        "release_version": settings.RELEASE_VERSION
    }


@app.get("/instance")
def instance():
    return {
        "container": socket.gethostname()
    }