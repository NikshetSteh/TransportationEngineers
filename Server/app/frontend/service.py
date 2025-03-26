from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from model.keycloak_users import KeycloakUser
from model.ticket import Ticket as TicketModel
from users.schemes import Ticket


async def k_id_to_user_id(
        k_id: str,
        db: sessionmaker[AsyncSession]
) -> str:
    async with db() as session:
        user = (await session.execute(
            select(KeycloakUser).where(KeycloakUser.k_id == k_id)
        )).one_or_none()
        if user is None:
            raise HTTPException(status_code=403, detail="Keycloak not linked")
        return user[0].user_id


async def get_user_last_ticket(
        k_user_id: str,
        db: sessionmaker[AsyncSession]
) -> Ticket | None:
    user_id = await k_id_to_user_id(k_user_id, db)

    async with db() as session:
        ticket_data = (await session.execute(
            select(TicketModel).where(TicketModel.user_id == user_id)
        )).one_or_none()

        if ticket_data is None:
            return ticket_data
        else:
            ticket = ticket_data[0]

            return Ticket(
                id=str(ticket.id),
                user_id=str(ticket.user_id),
                train_number=ticket.train_number,
                wagon_number=ticket.wagon_number,
                place_number=ticket.place_number,
                station_id=ticket.station_id,
                date=ticket.date,
                destination=ticket.destination_id,
                start_date=ticket.start_date,
            )
