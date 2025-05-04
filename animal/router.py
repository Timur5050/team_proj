from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import BackgroundTasks
from fastapi import APIRouter, Depends, HTTPException
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from auth.middleware import get_user_id
from database import AsyncSessionLocal
from dependencies import get_db, get_async_db
from animal.models import Animal
from animal.schemas import AnimalCreateSeparatelySchema, AnimalRetrieveSchema, AnimalCreateWithShelterSchema, \
    AnimalsListCreateSchema, AnimalListSchema
from animal import crud
from shelter.models import Shelter

router = APIRouter(prefix="/animal", tags=["animals"])


def check_unique_of_animals(
        shelter_id: int,
        animals: AnimalsListCreateSchema | AnimalCreateSeparatelySchema,
        db: Session
):
    animals_for_db = [animal.name for animal in db.query(Animal).filter(Animal.shelter_id == shelter_id)]

    if isinstance(animals, AnimalsListCreateSchema):
        duplicates = []
        for animal in animals.animals:
            if animal.name in animals_for_db:
                duplicates.append(animal.name)
        if duplicates:
            raise HTTPException(
                status_code=400,
                detail=f"This shelter already has animals with name(s): {', '.join(duplicates)}"
            )
    else:
        if animals.name in animals_for_db:
            raise HTTPException(
                status_code=400,
                detail=f"This shelter already has an animal with name: {animals.name}"
            )


@router.post("/", response_model=AnimalRetrieveSchema)
def create_animal(
        request: Request,
        animal: AnimalCreateSeparatelySchema,
        db: Session = Depends(get_db)
):
    user_id = get_user_id(request)

    shelter_from_db = db.query(Shelter).filter(Shelter.id == animal.shelter_id).first()
    if not shelter_from_db:
        raise HTTPException(status_code=404, detail="Shelter not found")

    if shelter_from_db.user_id != user_id:
        raise HTTPException(status_code=403, detail="You do not have access to this shelter")

    check_unique_of_animals(
        shelter_id=animal.shelter_id,
        animals=animal,
        db=db
    )

    return crud.create_animal(
        animal=animal,
        db=db
    )



@router.delete("/{shelter_id}/{animal_id}/", response_model=None)
def delete_animal(
        request: Request,
        animal_id: int,
        shelter_id: int,
        db: Session = Depends(get_db)
):
    user_id = get_user_id(request)

    shelter_from_db = db.query(Shelter).filter(Shelter.id == shelter_id).first()
    if not shelter_from_db:
        raise HTTPException(status_code=404, detail="Shelter not found")

    if shelter_from_db.user_id != user_id:
        raise HTTPException(status_code=403, detail="Access denied to this shelter")

    animal_from_db = db.query(Animal).filter(Animal.id == animal_id).first()
    if not animal_from_db or animal_from_db.shelter_id != shelter_id:
        raise HTTPException(status_code=404, detail="Animal not found in this shelter")

    crud.delete_animal(animal_id=animal_id, db=db)



@router.get("/{shelter_id}/", response_model=AnimalListSchema)
def get_animals_from_shelter(
        request: Request,
        shelter_id: int,
        db: Session = Depends(get_db),
        available: bool | None = None
):
    get_user_id(request)

    shelter = db.query(Shelter).filter(Shelter.id == shelter_id).first()
    if not shelter:
        raise HTTPException(status_code=404, detail="Shelter not found")

    animals = crud.get_animals_by_shelter(
        shelter_id=shelter_id,
        db=db,
        available=available
    )

    return {"animals": animals}


from fastapi import HTTPException, status

@router.get("/{shelter_id}/{animal_id}/", response_model=AnimalRetrieveSchema)
def retrieve_animal_by_id(
        request: Request,
        shelter_id: int,
        animal_id: int,
        db: Session = Depends(get_db)
):
    get_user_id(request)

    animal = crud.retrieve_animal_by_id(
        shelter_id=shelter_id,
        animal_id=animal_id,
        db=db
    )

    if animal is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Animal not found")

    return animal