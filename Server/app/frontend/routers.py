from fastapi import APIRouter, HTTPException

from db import DbDependency
from frontend.dependecies import KeycloakAuthRequired
from frontend.service import get_user_last_ticket
from users.schemes import Ticket

router = APIRouter()


@router.get("/get_ticket")
async def get_ticket(
        k_id: KeycloakAuthRequired,
        db: DbDependency
) -> Ticket:
    ticket = await get_user_last_ticket(
        k_id,
        db,
    )

    if ticket is None:
        raise HTTPException(status_code=404, detail="Ticket not found")

    return ticket
