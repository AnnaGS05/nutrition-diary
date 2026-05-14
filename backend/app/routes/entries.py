from datetime import date

from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import JSONResponse

from app.schemas.entry import EntryCreate
from app.services.auth_service import get_current_user_id
from app.services.entry_service import (
    get_entries,
    add_entry,
    delete_entry,
    get_stats
)

router = APIRouter(prefix="/api", tags=["Entries"])


@router.get("/entries/")
def entries(request: Request, entry_date: str | None = None):
    user_id = get_current_user_id(request)

    if not user_id:
        raise HTTPException(status_code=401, detail="Unauthorized")

    if not entry_date:
        entry_date = str(date.today())

    return JSONResponse(
        content=get_entries(user_id, entry_date),
        media_type="application/json; charset=utf-8"
    )


@router.post("/entries/")
def create_entry(entry: EntryCreate, request: Request):
    user_id = get_current_user_id(request)

    if not user_id:
        raise HTTPException(status_code=401, detail="Unauthorized")

    entry_data = entry.model_dump()

    if not entry_data["entry_date"]:
        entry_data["entry_date"] = str(date.today())
    else:
        entry_data["entry_date"] = str(entry_data["entry_date"])

    return JSONResponse(
        content=add_entry(user_id, entry_data),
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

    return {"message": "Entry deleted"}


@router.get("/stats")
def stats(request: Request, entry_date: str | None = None):
    user_id = get_current_user_id(request)

    if not user_id:
        raise HTTPException(status_code=401, detail="Unauthorized")

    if not entry_date:
        entry_date = str(date.today())

    return JSONResponse(
        content=get_stats(user_id, entry_date),
        media_type="application/json; charset=utf-8"
    )