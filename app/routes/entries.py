from fastapi import APIRouter
from app.services.entry_service import get_entries, add_entry

router = APIRouter(prefix="/api/entries", tags=["Entries"])

@router.get("/")
def read_entries():
    return get_entries()

@router.post("/")
def create_entry(entry: dict):
    return add_entry(entry)