from fastapi import APIRouter
from fastapi_pagination import paginate, Page

from db import DbDependency
from face_api.service import delete_face
from frontend.dependecies import KeycloakAuthRequired
from frontend.service import *
from schemes import EmptyResponse
from users.schemes import Ticket

router = APIRouter()


@router.get("/get_ticket")
async def get_ticket_router(user_id: KeycloakAuthRequired, db: DbDependency) -> Ticket:
    ticket = await get_user_last_ticket(
        user_id,
        db,
    )

    if ticket is None:
        raise HTTPException(status_code=404, detail="Ticket not found")

    return ticket


@router.get("/tickets")
async def get_tickets_router(user_id: KeycloakAuthRequired, db: DbDependency) -> Page[Ticket]:
    return paginate(await get_user_tickets(user_id, db))


@router.post("/faces")
async def add_face_router(
        user_id: KeycloakAuthRequired,
        file: UploadFile | None = None
) -> EmptyResponse:
    if file is not None:
        await create_face(file, user_id)
    else:
        await delete_face(user_id)

    return EmptyResponse()


@router.get("/faces")
async def check_face_for_existence_router(
        user_id: KeycloakAuthRequired
) -> EmptyResponse:
    is_exist = await check_face_for_existence(user_id)

    if not is_exist:
        raise HTTPException(status_code=404, detail="Face not found")

    return EmptyResponse()


@router.post("/tickets")
async def create_ticket_router(
        user_id: KeycloakAuthRequired, ticket_data: TicketCreation, db: DbDependency
) -> Ticket:
    return await create_ticket_simplified(ticket_data, user_id, db)
