from fastapi import APIRouter

from db import DbDependency
from face_api.service import delete_face, save_face
from frontend.dependecies import KeycloakAuthRequired
from frontend.schemes import Face
from frontend.service import *
from schemes import EmptyResponse
from users.schemes import Ticket

router = APIRouter()


@router.get("/get_ticket")
async def get_ticket(k_id: KeycloakAuthRequired, db: DbDependency) -> Ticket:
    ticket = await get_user_last_ticket(
        k_id,
        db,
    )

    if ticket is None:
        raise HTTPException(status_code=404, detail="Ticket not found")

    return ticket


@router.post("/face")
async def add_face(
        k_id: KeycloakAuthRequired, face: Face, db: DbDependency
) -> EmptyResponse:
    user_id = str(await k_id_to_user_id(k_id, db))

    if face.face is not None:
        await save_face(face.face, user_id)
    else:
        await delete_face(user_id)

    return EmptyResponse()


@router.post("/tickets")
async def create_ticket(
        ticket_data: TicketCreation, k_id: KeycloakAuthRequired, db: DbDependency
) -> Ticket:
    user_id = await k_id_to_user_id(k_id, db)

    return await create_ticket_simplified(ticket_data, user_id, db)
