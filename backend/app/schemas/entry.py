from datetime import date
from pydantic import BaseModel, Field, field_validator


class EntryCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    proteins: float = Field(default=0, ge=0, le=1000)
    fats: float = Field(default=0, ge=0, le=1000)
    carbs: float = Field(default=0, ge=0, le=1000)
    calories: float = Field(default=0, ge=0, le=10000)
    entry_date: date | None = None

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        if not isinstance(v, str):
            raise ValueError("invalid name")

        if len(v) < 1 or len(v) > 100:
            raise ValueError("invalid name")

        if not v.isprintable():
            raise ValueError("invalid name")

        return v