from fastapi import APIRouter, HTTPException, Path
from fastapi_pagination import Page, paginate

from auth.dependecies import RobotAuthRequired
from db import DbDependency
from robot.schemes import *
from robot.service import (check_user_place_in_wagon, get_current_ticket,
                           identification_face, get_hotels, get_attractions)
from users.schemes import Ticket, User

router = APIRouter()


@router.post("/identification")
async def identification(
        request: IdentificationRequest,
        db: DbDependency,
        _: RobotAuthRequired
) -> User:
    user = await identification_face(request.image, db)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return user


@router.post("/ticket_validation")
async def ticket_validation(
        request: TicketValidationRequest,
        db: DbDependency,
        _: RobotAuthRequired
) -> Ticket:
    user = await identification_face(request.face, db)
    if user is None:
        raise HTTPException(status_code=404, detail="Face not found")

    return await check_user_place_in_wagon(
        request.station_id,
        request.train_number,
        request.wagon_number,
        request.date,
        db
    )


@router.get("/station/{station_id}/user/{user_id}/current_ticket")
async def get_user_current_ticket(
        db: DbDependency,
        _: RobotAuthRequired,
        station_id: str,
        user_id: str = Path(pattern="^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$")
) -> Ticket:
    ticket = await get_current_ticket(user_id, station_id, db)
    if ticket is None:
        raise HTTPException(status_code=404, detail="Ticket not found")

    return ticket


@router.get("/destination/{destination_id}/hotels")
async def get_destination_hotels(
        db: DbDependency,
        _: RobotAuthRequired,
        destination_id: str
) -> list[Hotel]:
    return paginate(await get_hotels(destination_id, db))


@router.get("/destination/{destination_id}/attractions")
async def get_destination_attractions(
        destination_id: str,
        db: DbDependency,
        _: RobotAuthRequired
) -> Page[Attraction]:
    return paginate(await get_attractions(destination_id, db))
