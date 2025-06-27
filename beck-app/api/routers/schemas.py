from pydantic import BaseModel, Field
from typing import List
from enum import Enum


class BreedEnum(str, Enum):
    ABYSSINIAN = "Abyssinian"
    BENGAL = "Bengal"
    SIAMESE = "Siamese"

class CatCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)
    years_of_experience: int = Field(..., ge=0)
    breed: BreedEnum
    salary: int = Field(..., ge=0)

class CatUpdate(BaseModel):
    salary: int = Field(..., ge=0)

class CatResponse(BaseModel):
    id: int
    name: str
    years_of_experience: int
    breed: BreedEnum
    salary: int

    class Config:
        orm_mode = True

class TargetCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)
    country: str = Field(..., min_length=1, max_length=50)
    notes: str = Field(None, min_length=1, max_length=500)

class TargetUpdate(BaseModel):
    notes: str = Field(None, min_length=1, max_length=500)
    is_complete: bool = False

class MissionCreate(BaseModel):
    targets: List[TargetCreate]

class MissionResponse(BaseModel):
    id: int
    cat_id: int | None
    is_complete: bool
    targets: List[TargetCreate]

    class Config:
        orm_mode = True