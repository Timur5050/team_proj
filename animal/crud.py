import time

import simplejson as json

from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException

from animal.models import Animal, AnimalStatus
from animal.schemas import AnimalCreateSeparatelySchema, AnimalCreateWithShelterSchema, AnimalsListCreateSchema
from settings import settings


def create_animal(animal: AnimalCreateSeparatelySchema, db: Session) -> Animal:
    animal_obj = Animal(
        name=animal.name,
        age=animal.age,
        gender=animal.gender,
        description=animal.description,
        breed=animal.breed,
        character_traits=animal.character_traits,
        weight=animal.weight,
        height=animal.height,
        shelter_id=animal.shelter_id,
        status=AnimalStatus.AVAILABLE
    )

    db.add(animal_obj)
    db.commit()
    db.refresh(animal_obj)

    return animal_obj


def delete_animal(animal_id: int, db: Session):
    animal_to_delete = db.query(Animal).filter(Animal.id == animal_id).first()
    if not animal_to_delete:
        raise HTTPException(status_code=404, detail="Animal not found")

    db.delete(animal_to_delete)
    db.commit()



def get_animals_by_shelter(
        shelter_id: int,
        db: Session,
        available: bool | None
) -> list[Animal]:
    animal_queryset = db.query(Animal).filter(Animal.shelter_id == shelter_id).all()

    return animal_queryset


def retrieve_animal_by_id(
        shelter_id: int,
        animal_id: int,
        db: Session
) -> Animal:
    animal = db.query(Animal).filter(
        Animal.shelter_id == shelter_id,
        Animal.id == animal_id
    ).first()

    if not animal:
        raise HTTPException(status_code=404, detail="Animal not found")

    return animal