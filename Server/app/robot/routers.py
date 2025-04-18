from admin.schemes import Engineer
from auth.dependecies import RobotAuthRequired
from db import DbDependency
from fastapi import APIRouter, HTTPException, Path
from fastapi_pagination import Page, paginate
from robot.schemes import *
from robot.service import (check_ticket, check_user_place_in_wagon,
                           get_attractions, get_current_ticket, get_hotels,
                           get_train_stores, get_user_by_id,
                           get_user_destination_by_train, identification_face,
                           validate_robot_admin_access)
from schemes import TrainData
from store_api.schemes import Store
from users.schemes import Ticket, User

router = APIRouter()


@router.post("/identification")
async def identification(
    request: IdentificationRequest, db: DbDependency, _: RobotAuthRequired
) -> User:
    user = await identification_face(request.image, db)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return user


@router.post("/ticket_validation")
async def ticket_validation(
    request: TicketValidationRequest, db: DbDependency, _: RobotAuthRequired
) -> Ticket:
    if request.face is None and request.code is None:
        raise HTTPException(status_code=422)

    if request.face is not None:
        user = await identification_face(request.face, db)
        if user is None:
            raise HTTPException(status_code=404, detail="Face not found")

        return await check_user_place_in_wagon(
            request.station_id,
            request.train_number,
            request.wagon_number,
            request.date,
            str(user.id),
            db,
            request.mark_as_used,
        )
    if request.code is not None:
        return await check_ticket(
            request.station_id,
            request.train_number,
            request.wagon_number,
            request.date,
            request.code,
            db,
            request.mark_as_used,
        )


@router.post("/user/current_ticket")
async def get_user_current_ticket(
    db: DbDependency, _: RobotAuthRequired, request: UserLastTicketRequest
) -> Ticket:
    ticket = await get_current_ticket(
        request.user_id, request.train_id, request.start_date, db
    )

    if ticket is None:
        raise HTTPException(status_code=404, detail="Ticket not found")

    return ticket


@router.get("/destination/{destination_id}/hotels")
async def get_destination_hotels(
    db: DbDependency, _: RobotAuthRequired, destination_id: str
) -> Page[Hotel]:
    return paginate(await get_hotels(destination_id, db))


@router.get("/destination/{destination_id}/attractions")
async def get_destination_attractions(
    destination_id: str, db: DbDependency, _: RobotAuthRequired
) -> Page[Attraction]:
    return paginate(await get_attractions(destination_id, db))


@router.post("/engineer/admin_access")
async def admin_access(
    access_request: EngineerRobotAccessRequest, db: DbDependency, _: RobotAuthRequired
) -> Engineer:
    return await validate_robot_admin_access(access_request.key, db)


@router.post("/determine_destination")
async def get_user_destination(
    determination_request: DestinationDeterminationRequest,
    db: DbDependency,
    _: RobotAuthRequired,
) -> Destination:
    return await get_user_destination_by_train(
        determination_request.user_id,
        determination_request.train_number,
        determination_request.start_date,
        db,
    )


@router.get("/user/{user_id}")
async def get_user(
    db: DbDependency,
    _: RobotAuthRequired,
    user_id: str = Path(
        pattern="^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$"
    ),
) -> User:
    return await get_user_by_id(user_id, db)


@router.get("/train/stores")
async def get_train_stores_handler(
    train_data: TrainData, db: DbDependency, _: RobotAuthRequired
) -> list[Store]:
    return await get_train_stores(train_data.train_number, train_data.train_date, db)
