from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from dependencies import get_db
from shelter.models import Shelter
from shelter.schemas import ShelterCreateSchema, ShelterRetrieveSchema, ShelterDetailSchema
from auth.middleware import get_user_id
from shelter import crud
from user.models import User

router = APIRouter(prefix="/shelter", tags=["shelter"])


@router.post("/", response_model=ShelterRetrieveSchema)
def create_shelter(request: Request, shelter: ShelterCreateSchema, db: Session = Depends(get_db)):
    user_id = get_user_id(request)

    if db.query(Shelter).filter(Shelter.title == shelter.title).first():
        raise HTTPException(status_code=400, detail="This title is already taken")

    return crud.create_shelter(
        shelter=shelter,
        user_id=user_id,
        db=db
    )


@router.get("/shelters/", response_model=list[ShelterRetrieveSchema])
def get_all_shelters(request: Request, my: bool = False, db: Session = Depends(get_db)):
    if my:
        user_id = get_user_id(request)
        return crud.get_current_user_shelter_list(
            db=db,
            user_id=user_id
        )
    return crud.get_all_shelters(
        db=db
    )


@router.get("/shelters/{shelter_id}/", response_model=ShelterDetailSchema)
def get_details_of_shelter(request: Request, shelter_id: int, db: Session = Depends(get_db)):
    get_user_id(request)

    try:
        return crud.get_details_of_shelter(
            db=db,
            shelter_id=shelter_id
        )
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=500, detail="Unexpected error retrieving shelter details")


@router.post(
    "/shelters/{shelter_id}/{approve}/",
    response_model=ShelterRetrieveSchema,
    responses={400: {"description": "You are not admin"}}
)
def change_shelters_status(
        request: Request,
        shelter_id: int,
        approve: int,
        db: Session = Depends(get_db)
):
    user_id = get_user_id(request)
    user = db.query(User).get(user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if not user.is_superuser:
        raise HTTPException(status_code=403, detail="You are not authorized to approve shelters")

    return crud.change_shelters_status(
        db=db,
        shelter_id=shelter_id,
        approve=approve
    )


@router.delete("/shelters/{shelter_id}/", status_code=204)
def delete_shelter(
        request: Request,
        shelter_id: int,
        db: Session = Depends(get_db)
):
    user_id = get_user_id(request)
    user = db.query(User).get(user_id)

    crud.delete_shelter(db=db, shelter_id=shelter_id, current_user=user)

    return None