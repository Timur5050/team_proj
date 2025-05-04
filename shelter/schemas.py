from pydantic import BaseModel, field_validator

from animal.schemas import AnimalCreateWithShelterSchema, AnimalRetrieveSchema
from shelter.models import ShelterStatus

class ShelterCreateSchema(BaseModel):
    title: str
    address: str
    description: str | None
    contacts: str
    animals: list[AnimalCreateWithShelterSchema] | None = None

class ShelterRetrieveSchema(BaseModel):
    id: int
    title: str
    address: str
    description: str
    contacts: str
    status: str
    user_id: int


class ShelterDetailSchema(ShelterRetrieveSchema):
    animals: list[AnimalRetrieveSchema]