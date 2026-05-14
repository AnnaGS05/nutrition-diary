from datetime import date
from pydantic import BaseModel, Field


class EntryCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    proteins: float = Field(default=0, ge=0, le=1000)
    fats: float = Field(default=0, ge=0, le=1000)
    carbs: float = Field(default=0, ge=0, le=1000)
    calories: float = Field(default=0, ge=0, le=10000)
    entry_date: date | None = None