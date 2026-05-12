from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import JSONResponse

from app.services.auth_service import get_current_user_id
from app.services.entry_service import (
    get_entries,
    add_entry,
    delete_entry,
    get_stats
)

router = APIRouter(prefix="/api", tags=["Entries"])


@router.get("/entries/")
def entries(request: Request):
    user_id = get_current_user_id(request)

    if not user_id:
        raise HTTPException(status_code=401, detail="Unauthorized")

    return JSONResponse(
        content=get_entries(user_id),
        media_type="application/json; charset=utf-8"
    )


@router.post("/entries/")
def create_entry(entry: dict, request: Request):
    user_id = get_current_user_id(request)

    if not user_id:
        raise HTTPException(status_code=401, detail="Unauthorized")

    return JSONResponse(
        content=add_entry(user_id, entry),
        media_type="application/json; charset=utf-8"
    )


@router.delete("/entries/{entry_id}")
def remove_entry(entry_id: int, request: Request):
    user_id = get_current_user_id(request)

    if not user_id:
        raise HTTPException(status_code=401, detail="Unauthorized")

    deleted = delete_entry(user_id, entry_id)

    if not deleted:
        raise HTTPException(status_code=404, detail="Entry not found")

    return JSONResponse(
        content={"message": "Entry deleted"},
        media_type="application/json; charset=utf-8"
    )


@router.get("/stats")
def stats(request: Request):
    user_id = get_current_user_id(request)

    if not user_id:
        raise HTTPException(status_code=401, detail="Unauthorized")

    return JSONResponse(
        content=get_stats(user_id),
        media_type="application/json; charset=utf-8"
    )