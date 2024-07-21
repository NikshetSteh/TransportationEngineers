from fastapi import APIRouter, HTTPException

from auth.dependecies import AuthRequired
from db import DbDependency
from robot.schemes import *
from robot.service import check_user_place_in_wagon, identification_face
from users.schemes import Ticket, User

router = APIRouter()


@router.post("/identification")
async def identification(
        request: IdentificationRequest,
        db: DbDependency,
        _: AuthRequired
) -> User:
    user = await identification_face(request.image, db)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return user


@router.post("/ticket_validation")
async def ticket_validation(
        request: TicketValidationRequest,
        db: DbDependency,
        _: AuthRequired
) -> Ticket:
    user = await identification_face(request.face, db)
    if user is None:
        raise HTTPException(status_code=404, detail="Face not found")

    return await check_user_place_in_wagon(
        request.train_number,
        request.wagon_number,
        request.date,
        db
    )
