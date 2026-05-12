import socket

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.config import settings
from app.middleware import RequestLoggingMiddleware
from app.routes.auth import router as auth_router
from app.routes.entries import router as entries_router
from app.routes.profile import router as profile_router
from app.routes.stats import router as stats_router

app = FastAPI(
    title=settings.APP_NAME,
    default_response_class=JSONResponse
)

app.add_middleware(RequestLoggingMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(entries_router)
app.include_router(profile_router)
app.include_router(stats_router)


@app.get("/")
def root():
    return {"message": "NutriLog API"}


@app.get("/health")
def health():
    return JSONResponse(
        content={
            "status": "ok",
            "environment": settings.ENVIRONMENT,
            "release_version": settings.RELEASE_VERSION
        },
        media_type="application/json; charset=utf-8"
    )


@app.get("/instance")
def instance():
    return JSONResponse(
        content={
            "container": socket.gethostname()
        },
        media_type="application/json; charset=utf-8"
    )