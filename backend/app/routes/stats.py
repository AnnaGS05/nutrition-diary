from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import JSONResponse

from app.services.auth_service import get_current_user_id
from app.services.stats_service import get_weekly_stats

router = APIRouter(prefix="/api/stats", tags=["Stats"])


@router.get("/weekly")
def weekly_stats(request: Request):
    user_id = get_current_user_id(request)

    if not user_id:
        raise HTTPException(status_code=401, detail="Unauthorized")

    return JSONResponse(
        content=get_weekly_stats(user_id),
        media_type="application/json; charset=utf-8"
    )
