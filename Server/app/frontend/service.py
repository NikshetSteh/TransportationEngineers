import random

from config import get_config
from fastapi import HTTPException
from frontend.schemes import TicketCreation
from model.keycloak_users import KeycloakUser
from model.ticket import Ticket as TicketModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from users.schemes import Ticket


async def k_id_to_user_id(k_id: str, db: sessionmaker[AsyncSession]) -> str:
    async with db() as session:
        user = (
            await session.execute(select(KeycloakUser).where(KeycloakUser.k_id == k_id))
        ).one_or_none()
        if user is None:
            raise HTTPException(status_code=403, detail="Keycloak not linked")
        return user[0].user_id


async def get_user_last_ticket(
    k_user_id: str, db: sessionmaker[AsyncSession]
) -> Ticket | None:
    user_id = await k_id_to_user_id(k_user_id, db)

    async with db() as session:
        ticket_data = (
            await session.execute(
                select(TicketModel)
                .where(TicketModel.user_id == user_id)
                .order_by(TicketModel.date.desc())
                .limit(1)
            )
        ).one_or_none()

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
                code=ticket.code,
            )


async def create_ticket_simplified(
    ticket_data: TicketCreation, user_id: str, db: sessionmaker[AsyncSession]
) -> Ticket:
    config = get_config()

    async with db() as session:
        # Check for existence of tickets
        tickets = await session.execute(
            select(TicketModel)
            .where(
                TicketModel.train_number == ticket_data.train_number,
                TicketModel.wagon_number == ticket_data.wagon_number,
                TicketModel.place_number == ticket_data.place_number,
                TicketModel.date == ticket_data.date,
                TicketModel.start_date == ticket_data.date,
            )
            .limit(1)
        )
        tickets = tickets.scalar()
        if tickets is not None:
            raise HTTPException(status_code=409, detail="Ticket already exists")

        ticket_model = TicketModel(
            user_id=user_id,
            train_number=ticket_data.train_number,
            wagon_number=ticket_data.wagon_number,
            place_number=ticket_data.place_number,
            date=ticket_data.date,
            station_id=ticket_data.station_id.value,
            code="".join(random.choices(config.SYMBOLS_POOL, k=config.TICKET_CODE_LEN)),
            destination_id=ticket_data.station_id.value,
            start_date=ticket_data.date,
            used=False,
        )
        session.add(ticket_model)
        await session.commit()

        return Ticket(
            id=str(ticket_model.id),
            user_id=str(ticket_model.user_id),
            train_number=ticket_model.train_number,
            wagon_number=ticket_model.wagon_number,
            place_number=ticket_model.place_number,
            station_id=ticket_model.station_id,
            date=ticket_model.date,
            destination=ticket_model.destination_id,
            start_date=ticket_model.start_date,
            code=ticket_model.code,
        )
