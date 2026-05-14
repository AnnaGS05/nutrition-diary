from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import JSONResponse

from app.schemas.profile import ProfileCreate
from app.services.auth_service import get_current_user_id
from app.services.profile_service import save_profile, get_profile

router = APIRouter(prefix="/api/profile", tags=["Profile"])


@router.get("/")
def profile(request: Request):
    user_id = get_current_user_id(request)

    if not user_id:
        raise HTTPException(status_code=401, detail="Unauthorized")

    data = get_profile(user_id)

    if not data:
        return JSONResponse(
            content={"exists": False},
            media_type="application/json; charset=utf-8"
        )

    data["exists"] = True

    return JSONResponse(
        content=data,
        media_type="application/json; charset=utf-8"
    )


@router.post("/")
def create_or_update_profile(profile_data: ProfileCreate, request: Request):
    user_id = get_current_user_id(request)

    if not user_id:
        raise HTTPException(status_code=401, detail="Unauthorized")

    norms = save_profile(user_id, profile_data.model_dump())

    return JSONResponse(
        content={
            "message": "Profile saved",
            **norms
        },
        media_type="application/json; charset=utf-8"
    )