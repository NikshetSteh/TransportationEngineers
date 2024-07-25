import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload, sessionmaker

from admin.schemes import Engineer
from auth.engineer_privileges import (EngineerPrivileges,
                                      engineer_privileges_translations)
from face_api.service import search_face
from model.auth_cards import AuthCard
from model.engineer import Engineer as EngineerModel
from model.ticket import Ticket as TicketModel
from model.user import User as UserModel
from robot.exceptions import *
from users.schemes import Ticket, User


async def identification_face(
        face: str,
        db: sessionmaker[AsyncSession]
) -> User | None:
    user_id = await search_face(face)

    if user_id is None:
        return None

    async with db() as session:
        users = (await session.execute(
            select(UserModel).where(UserModel.id == user_id)
        )).one_or_none()

        if users is None:
            return None

        user = users[0]

    return User(id=user_id, name=user.name)


async def check_user_place_in_wagon(
        station_id: str,
        train_number: int,
        wagon_number: int,
        date: datetime.datetime,
        db: sessionmaker[AsyncSession]
) -> Ticket:
    async with db() as session:
        tickets = (await session.execute(
            select(TicketModel).where(
                TicketModel.train_number == train_number,
                TicketModel.wagon_number == wagon_number,
                TicketModel.date == date,
                TicketModel.station_id == station_id
            ).limit(1)
        )).one_or_none()

        if tickets is not None:
            return Ticket(
                id=str(tickets[0].id),
                user_id=str(tickets[0].user_id),
                train_number=tickets[0].train_number,
                wagon_number=tickets[0].wagon_number,
                place_number=tickets[0].place_number,
                station_id=tickets[0].station_id,
                date=tickets[0].date
            )

        tickets = (await session.execute(
            select(TicketModel).where(
                TicketModel.train_number == train_number,
                TicketModel.wagon_number != wagon_number,
                TicketModel.date == date,
                TicketModel.station_id == station_id
            ).limit(1)
        )).one_or_none()

        if tickets is not None:
            raise InvalidTicketWagon(Ticket(
                id=str(tickets[0].id),
                user_id=str(tickets[0].user_id),
                train_number=tickets[0].train_number,
                wagon_number=tickets[0].wagon_number,
                place_number=tickets[0].place_number,
                station_id=tickets[0].station_id,
                date=tickets[0].date
            ))

        tickets = (await session.execute(
            select(TicketModel).where(
                TicketModel.train_number == train_number,
                TicketModel.date >= date,
                TicketModel.station_id == station_id
            ).limit(1)
        )).one_or_none()

        if tickets is not None:
            raise InvalidTicketDate(Ticket(
                id=str(tickets[0].id),
                user_id=str(tickets[0].user_id),
                train_number=tickets[0].train_number,
                wagon_number=tickets[0].wagon_number,
                place_number=tickets[0].place_number,
                station_id=tickets[0].station_id,
                date=tickets[0].date
            ))

        tickets = (await session.execute(
            select(TicketModel).where(
                TicketModel.date >= date
            ).limit(1)
        )).one_or_none()

        if tickets is not None:
            raise InvalidTicketTrain(Ticket(
                id=str(tickets[0].id),
                user_id=str(tickets[0].user_id),
                train_number=tickets[0].train_number,
                wagon_number=tickets[0].wagon_number,
                place_number=tickets[0].place_number,
                station_id=tickets[0].station_id,
                date=tickets[0].date
            ))

        raise InvalidWithoutTickets()


async def get_current_ticket(
        user_id: str,
        station_id: str,
        db: sessionmaker[AsyncSession]
) -> Ticket | None:
    async with db() as session:
        now_datetime = datetime.datetime.now()
        tickets = (await session.execute(
            select(TicketModel).where(
                TicketModel.date >= now_datetime,
                station_id == TicketModel.station_id,
                user_id == TicketModel.user_id
            )
        )).one_or_none()

        if tickets is None:
            return None

        return Ticket(
            id=str(tickets[0].id),
            user_id=str(tickets[0].user_id),
            train_number=tickets[0].train_number,
            wagon_number=tickets[0].wagon_number,
            place_number=tickets[0].place_number,
            station_id=tickets[0].station_id,
            date=tickets[0].date
        )


async def validate_robot_admin_access(
        key: str,
        db: sessionmaker[AsyncSession]
) -> Engineer:
    async with db() as session:
        auth_cards = (await session.execute(
            select(AuthCard).where(
                AuthCard.key == key
            ).options(selectinload(AuthCard.engineer))
        )).one_or_none()

        if auth_cards is None:
            raise HTTPException(status_code=403, detail="Access denied")

        engineer_model: EngineerModel = auth_cards[0].engineer

        if engineer_model.privileges & engineer_privileges_translations[EngineerPrivileges.ROBOT_ADMIN] == 0:
            raise HTTPException(status_code=403, detail="Access denied")

        engineer = Engineer(
            id=str(engineer_model.id),
            login=engineer_model.login
        )

        return engineer
