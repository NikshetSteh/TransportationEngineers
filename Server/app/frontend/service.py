import random

from config import get_config
from fastapi import HTTPException
from frontend.schemes import Station, TicketCreation, PasswordChangeRequest
from model.ticket import Ticket as TicketModel
from model.user import User as UserModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from users.schemes import Ticket

from bcrypt import checkpw, hashpw, gensalt


async def get_user_last_ticket(
        user_id: str, db: sessionmaker[AsyncSession]
) -> Ticket | None:
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

    # Fix
    if ticket_data.station_id == Station.MOSCOW:
        if ticket_data.date.hour == 5:
            ticket_data.train_number = 1012
        elif ticket_data.date.hour == 9:
            ticket_data.train_number = 1013
        elif ticket_data.date.hour == 13:
            ticket_data.train_number = 1014
        elif ticket_data.date.hour == 17:
            ticket_data.train_number = 1015
        else:
            raise HTTPException(status_code=400, detail="Invalid time")
    else:
        if ticket_data.date.hour == 5:
            ticket_data.train_number = 2012
        elif ticket_data.date.hour == 9:
            ticket_data.train_number = 2013
        elif ticket_data.date.hour == 13:
            ticket_data.train_number = 2014
        elif ticket_data.date.hour == 17:
            ticket_data.train_number = 2015
        else:
            raise HTTPException(status_code=400, detail="Invalid time")

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
            destination_id=ticket_data.destination_id.value,
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
