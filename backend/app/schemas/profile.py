from typing import Literal
from pydantic import BaseModel, Field


class ProfileCreate(BaseModel):
    age: int = Field(..., ge=10, le=120)
    height: float = Field(..., ge=100, le=250)
    weight: float = Field(..., ge=30, le=300)
    gender: Literal["male", "female"]
    activity: float = Field(..., ge=1.2, le=1.9)
    goal: Literal["loss", "maintain", "gain"]