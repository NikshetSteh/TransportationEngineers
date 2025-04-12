from fastapi import APIRouter

from db import DbDependency
from face_api.service import delete_face, save_face
from frontend.dependecies import KeycloakAuthRequired
from frontend.schemes import Face, PasswordChangeRequest
from frontend.service import *
from schemes import EmptyResponse
from users.schemes import Ticket

router = APIRouter()


@router.get("/get_ticket")
async def get_ticket(user_id: KeycloakAuthRequired, db: DbDependency) -> Ticket:
    ticket = await get_user_last_ticket(
        user_id,
        db,
    )

    if ticket is None:
        raise HTTPException(status_code=404, detail="Ticket not found")

    return ticket


@router.post("/face")
async def add_face(
        user_id: KeycloakAuthRequired, face: Face
) -> EmptyResponse:
    if face.face is not None:
        await save_face(face.face, user_id)
    else:
        await delete_face(user_id)

    return EmptyResponse()


@router.post("/tickets")
async def create_ticket(
        user_id: KeycloakAuthRequired, ticket_data: TicketCreation, db: DbDependency
) -> Ticket:
    return await create_ticket_simplified(ticket_data, user_id, db)
