from fastapi import HTTPException

import simplejson as json
from sqlalchemy.orm import Session

from animal.models import Animal as AnimalModel, Animal
from shelter.models import Shelter, ShelterStatus
from settings import settings
from shelter.models import ShelterStatus
from animal.models import AnimalStatus

from shelter.schemas import ShelterCreateSchema, ShelterRetrieveSchema, ShelterDetailSchema
from user.models import User


def create_shelter(shelter: ShelterCreateSchema, user_id: int, db: Session) -> ShelterRetrieveSchema:
    shelter_obj = Shelter(
        title=shelter.title,
        address=shelter.address,
        description=shelter.description,
        contacts=shelter.contacts,
        status=ShelterStatus.PENDING,
        user_id=user_id
    )
    db.add(shelter_obj)
    db.commit()
    db.refresh(shelter_obj)

    if shelter.animals:
        for animal in shelter.animals:
            print("character_traits:", Animal.character_traits)
            animal_obj = AnimalModel(
                name=animal.name,
                age=animal.age,
                gender=animal.gender,
                description=animal.description,
                breed=animal.breed,
                character_traits=animal.character_traits,
                weight=animal.weight,
                height=animal.height,
                status=AnimalStatus.AVAILABLE,
                shelter_id=shelter_obj.id
            )
            db.add(animal_obj)
            db.commit()
            db.refresh(animal_obj)


    return ShelterRetrieveSchema(**shelter_obj.to_dict())


def get_all_shelters(db: Session) -> list[ShelterRetrieveSchema]:
    shelters = db.query(Shelter).all()
    shelter_dicts = [shelter.to_dict() for shelter in shelters]

    return [ShelterRetrieveSchema(**shelter) for shelter in shelter_dicts]


def get_current_user_shelter_list(db: Session, user_id: int) -> list[ShelterRetrieveSchema]:
    shelters = db.query(Shelter).filter(Shelter.user_id == user_id).all()
    shelter_dicts = [shelter.to_dict() for shelter in shelters]

    return [ShelterRetrieveSchema(**shelter) for shelter in shelter_dicts]


def get_details_of_shelter(db: Session, shelter_id: int) -> ShelterDetailSchema:
    shelter_obj = db.query(Shelter).filter(Shelter.id == shelter_id).first()
    if not shelter_obj:
        raise HTTPException(status_code=404, detail="Shelter not found")

    animals = db.query(AnimalModel).filter(AnimalModel.shelter_id == shelter_id).all()
    shelter_dict = shelter_obj.to_dict()
    shelter_dict["animals"] = [animal.to_dict() for animal in animals]

    return ShelterDetailSchema(**shelter_dict)


def change_shelters_status(db: Session, shelter_id: int, approve: int):
    shelter_obj = db.query(Shelter).filter(Shelter.id == shelter_id).first()
    if not shelter_obj:
        raise HTTPException(status_code=404, detail="Shelter not found")

    if approve:
        shelter_obj.status = ShelterStatus.APPROVED
    else:
        shelter_obj.status = ShelterStatus.REJECTED

    db.commit()
    db.refresh(shelter_obj)

    return ShelterRetrieveSchema(**shelter_obj.to_dict())


def delete_shelter(db: Session, shelter_id: int, current_user: User):
    shelter = db.query(Shelter).filter(Shelter.id == shelter_id).first()

    if not shelter:
        raise HTTPException(status_code=404, detail="Shelter not found")

    if not current_user.is_superuser and shelter.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this shelter")

    db.delete(shelter)
    db.commit()
