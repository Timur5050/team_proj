import decimal
from decimal import Decimal
from enum import Enum

from pydantic import BaseModel, field_validator


class AnimalGender(str, Enum):
    FEMALE = "female"
    MALE = "male"


class AnimalStatus(str, Enum):
    AVAILABLE = "available"
    ADOPTED = "adopted"


class AnimalCreateWithShelterSchema(BaseModel):
    name: str
    age: int
    gender: AnimalGender
    description: str | None = None
    breed: str
    character_traits: str
    weight: Decimal
    height: Decimal


class AnimalCreateSeparatelySchema(AnimalCreateWithShelterSchema):
    shelter_id: int


class AnimalRetrieveSchema(BaseModel):
    id: int
    name: str
    age: int
    gender: AnimalGender
    description: str | None = None
    shelter_id: int
    breed: str
    character_traits: str
    weight: Decimal
    height: Decimal
    status: AnimalStatus

    @field_validator("age")
    def validate_age(cls, v):
        if not (0 <= v <= 100):
            raise ValueError("Age must be between 0 and 100")
        return v

    @field_validator("weight")
    def validate_weight(cls, v):
        if not (0 <= v <= 200):
            raise ValueError("Weight must be between 0 and 200")
        return v

    @field_validator("height")
    def validate_height(cls, v):
        if not (0 <= v <= 200):
            raise ValueError("Height must be between 0 and 200")
        return v

    @field_validator("name", "breed", "character_traits")
    def validate_non_empty_strings(cls, v):
        if not v or not v.strip():
            raise ValueError("Field cannot be empty")
        return v

    class Config:
        orm_mode = True


class AnimalsListCreateSchema(BaseModel):
    animals: list[AnimalCreateWithShelterSchema]


class AnimalListSchema(BaseModel):
    animals: list[AnimalRetrieveSchema]