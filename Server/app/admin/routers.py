import bcrypt
from fastapi import APIRouter, HTTPException, Path
from fastapi_pagination import Page, paginate
from sqlalchemy import delete, select

from admin.schemes import *
from auth.engineer_privileges import engineer_privileges_translations
from db import DbDependency
from face_api.service import delete_face, save_face
from model.auth_cards import AuthCard as AuthCardModel
from model.destinations_info import Attraction as AttractionModel
from model.destinations_info import Hotel as HotelModel
from model.engineer import Engineer as EngineerModel
from model.robot import Robot as RobotModel
from model.ticket import Ticket as TicketModel
from model.user import User as UserModel
from robot.schemes import Attraction, Hotel, Robot
from robot.service import get_attractions, get_hotels
from schemes import EmptyResponse
from users.schemes import Ticket, TicketCreation, User

router = APIRouter()


@router.post("/user")
async def add_user(
        data: UserCreation,
        db: DbDependency
) -> User:
    async with db() as session:
        users = (await session.execute(
            select(UserModel).where(UserModel.name == data.name)
        )).one_or_none()

        if users is not None:
            raise HTTPException(status_code=409, detail="User already exists")

        user = UserModel(
            name=data.name
        )
        session.add(user)
        await session.flush()

        if data.face is not None:
            await save_face(data.face, str(user.id))

        await session.commit()

    return User(id=str(user.id), name=data.name)


@router.patch("/user/{user_id}/face")
async def update_user_face(
        user_id: str,
        data: UserFaceUpdate,
        db: DbDependency
) -> EmptyResponse:
    async with db() as session:
        user = (await session.execute(
            select(UserModel).where(UserModel.id == user_id)
        )).one_or_none()

        if user is None:
            raise HTTPException(status_code=404, detail="User not found")

        if data.face is not None:
            await save_face(data.face, user_id)

        session.add(user)
        await session.commit()

    return EmptyResponse()


@router.delete("/user/face")
async def delete_user_face(
        user_id: str,
        db: DbDependency
) -> EmptyResponse:
    async with db() as session:
        user = (await session.execute(
            select(UserModel).where(UserModel.id == user_id)
        )).one_or_none()

        if user is None:
            raise HTTPException(status_code=404, detail="User not found")

        await delete_face(user_id)

        session.add(user)
        await session.commit()

    return EmptyResponse()


@router.get("/users")
async def get_users(
        db: DbDependency
) -> Page[User]:
    async with db() as session:
        users = (await session.execute(
            select(UserModel)
        )).fetchall()

    data = list(
        map(
            lambda x: User(
                id=str(x[0].id),
                name=x[0].name
            ),
            users
        )
    )

    return paginate(data)


@router.delete("/users/{user_id}")
async def delete_user(
        user_id: str,
        db: DbDependency
) -> EmptyResponse:
    async with db() as session:
        user = (await session.execute(
            select(UserModel).where(UserModel.id == user_id)
        )).one_or_none()

        if user is None:
            raise HTTPException(status_code=404, detail="User not found")

        await session.execute(
            delete(TicketModel).where(TicketModel.user_id == user_id)
        )
        await session.execute(
            delete(UserModel).where(UserModel.id == user_id)
        )
        await session.commit()

    await delete_face(user_id)

    return EmptyResponse()


@router.post("/engineer")
async def create_engineer(
        data: EngineerCreation,
        db: DbDependency
) -> Engineer:
    async with db() as session:
        hashed_password = bcrypt.hashpw(
            data.password.encode("utf-8"),
            bcrypt.gensalt(12)
        ).decode("utf-8")

        engineer = EngineerModel(
            login=data.login,
            password=hashed_password
        )
        session.add(engineer)
        await session.commit()

    return Engineer(
        id=str(engineer.id),
        login=engineer.login
    )


@router.delete("/engineers/{engineer_id}")
async def delete_engineer(
        engineer_id: str,
        db: DbDependency
) -> EmptyResponse:
    async with db() as session:
        print(engineer_id)
        engineers = (await session.execute(
            select(EngineerModel).where(EngineerModel.id == engineer_id)
        )).one_or_none()

        if engineers is None:
            raise HTTPException(status_code=404, detail="Engineer not found")

        await session.execute(
            delete(EngineerModel).where(EngineerModel.id == engineer_id)
        )
        await session.commit()

    return EmptyResponse()


@router.get("/engineers")
async def get_engineer(
        db: DbDependency
) -> Page[Engineer]:
    async with db() as session:
        engineers = (await session.execute(
            select(EngineerModel)
        )).fetchall()

    data = list(
        map(
            lambda x: Engineer(
                id=str(x[0].id),
                login=x[0].login
            ),
            engineers
        )
    )
    return paginate(data)


@router.put("/engineer_privileges")
async def update_engineer(
        data: EngineerPrivilegesUpdate,
        db: DbDependency
) -> EmptyResponse:
    async with db() as session:
        engineers = (await session.execute(
            select(EngineerModel).where(EngineerModel.id == data.id)
        )).one_or_none()

        if engineers is None:
            raise HTTPException(status_code=404, detail="Engineer not found")

        engineer = engineers[0]

        privileges = 0
        for i in data.privileges:
            privileges |= engineer_privileges_translations[i]

        engineer.privileges = privileges
        session.add(engineer)
        await session.commit()

    return EmptyResponse()


@router.get("/robots")
async def get_robots(
        db: DbDependency
) -> Page[Robot]:
    async with db() as session:
        robots = (await session.execute(
            select(RobotModel)
        )).fetchall()

    data = list(
        map(
            lambda x: Robot(
                id=str(x[0].id),
                robot_model_name=x[0].robot_model_name,
                robot_model_id=x[0].robot_model_id,
            ),
            robots
        )
    )
    return paginate(data)


@router.delete("/robots/{robot_id}")
async def delete_robot(
        robot_id: str,
        db: DbDependency
) -> EmptyResponse:
    async with db() as session:
        await session.execute(
            delete(RobotModel).where(RobotModel.id == robot_id)
        )
        await session.commit()

    return EmptyResponse()


@router.post("/ticket")
async def create_ticket(
        data: TicketCreation,
        db: DbDependency
) -> Ticket:
    async with db() as session:
        users = (await session.execute(
            select(UserModel).where(UserModel.id == data.user_id)
        )).one_or_none()

        if users is None:
            raise HTTPException(status_code=404, detail="User not found")

        ticket = TicketModel(
            user_id=data.user_id,
            train_number=data.train_number,
            wagon_number=data.wagon_number,
            place_number=data.place_number,
            station_id=data.station_id,
            date=data.date,
            destination_id=data.destination
        )
        session.add(ticket)
        await session.commit()

    return Ticket(
        id=str(ticket.id),
        user_id=ticket.user_id,
        train_number=ticket.train_number,
        wagon_number=ticket.wagon_number,
        place_number=ticket.place_number,
        station_id=ticket.station_id,
        date=ticket.date,
        destination=ticket.destination_id
    )


@router.delete("/ticket/{ticket_id}")
async def delete_ticket(
        ticket_id: str,
        db: DbDependency
) -> EmptyResponse:
    async with db() as session:
        await session.execute(
            delete(TicketModel).where(TicketModel.id == ticket_id)
        )
        await session.commit()

    return EmptyResponse()


@router.get("/tickets")
async def get_tickets(
        db: DbDependency
) -> Page[Ticket]:
    async with db() as session:
        tickets = (await session.execute(
            select(TicketModel)
        )).fetchall()

    data = list(
        map(
            lambda x: Ticket(
                id=str(x[0].id),
                user_id=str(x[0].user_id),
                train_number=x[0].train_number,
                wagon_number=x[0].wagon_number,
                place_number=x[0].place_number,
                station_id=x[0].station_id,
                date=x[0].date,
                destination=x[0].destination_id
            ),
            tickets
        )
    )
    return paginate(data)


@router.get("/destination/{destination_id}/hotels")
async def get_destination_hotels(
        db: DbDependency,
        destination_id: str
) -> Page[Hotel]:
    return paginate(await get_hotels(destination_id, db))


@router.get("/destination/{destination_id}/attractions")
async def get_destination_attractions(
        destination_id: str,
        db: DbDependency,
) -> Page[Attraction]:
    return paginate(await get_attractions(destination_id, db))


@router.post("/destination/{destination_id}/hotel")
async def create_destination_hotel(
        destination_id: str,
        data: HotelCreation,
        db: DbDependency
) -> Hotel:
    async with db() as session:
        hotel = HotelModel(
            destination_id=destination_id,
            name=data.name,
            description=data.description,
            logo_url=data.logo_url
        )
        session.add(hotel)
        await session.commit()

    return Hotel(
        id=str(hotel.id),
        name=hotel.name,
        description=hotel.description,
        logo_url=hotel.logo_url
    )


@router.post("/destination/{destination_id}/attraction")
async def create_destination_attraction(
        destination_id: str,
        data: AttractionCreation,
        db: DbDependency
) -> Attraction:
    async with db() as session:
        attraction = AttractionModel(
            destination_id=destination_id,
            name=data.name,
            description=data.description,
            logo_url=data.logo_url
        )
        session.add(attraction)
        await session.commit()

    return Attraction(
        id=str(attraction.id),
        name=attraction.name,
        description=attraction.description,
        logo_url=attraction.logo_url
    )


@router.delete("/destination_info/hotel/{hotel_id}")
async def delete_destination_hotel(
        hotel_id: str,
        db: DbDependency
) -> EmptyResponse:
    async with db() as session:
        await session.execute(
            delete(HotelModel).where(HotelModel.id == hotel_id)
        )
        await session.commit()

    return EmptyResponse()


@router.delete("/destination_info/attraction/{attraction_id}")
async def delete_destination_attraction(
        attraction_id: str,
        db: DbDependency
) -> EmptyResponse:
    async with db() as session:
        await session.execute(
            delete(AttractionModel).where(AttractionModel.id == attraction_id)
        )
        await session.commit()
    return EmptyResponse()


@router.put("/engineer/{engineer_id}/auth_card")
async def update_auth_card(
        data: AuthCardCreation,
        db: DbDependency,
        engineer_id: str = Path(pattern="[a-f0-9]{8}-[a-f0-9]{4}-4[a-f0-9]{3}-[89ab][a-f0-9]{3}-[a-f0-9]{12}")
) -> EmptyResponse:
    async with db() as session:
        engineers = (await session.execute(
            select(EngineerModel).where(EngineerModel.id == engineer_id)
        )).one_or_none()
        if engineers is None:
            raise HTTPException(status_code=404, detail="Engineer not found")

        if data.key is None or data.key == "":
            await session.execute(
                delete(AuthCardModel).where(AuthCardModel.engineer_id == engineer_id)
            )
            await session.commit()
            return EmptyResponse()

        auth_cards = (await session.execute(
            select(AuthCardModel).where(AuthCardModel.engineer_id == engineer_id)
        )).one_or_none()
        if auth_cards is not None:
            auth_card = auth_cards[0]
            auth_card.key = data.key
            session.add(auth_card)
            await session.commit()
            return EmptyResponse()

        auth_card = AuthCardModel(
            engineer_id=engineer_id,
            key=data.key
        )
        session.add(auth_card)
        await session.commit()

    return EmptyResponse()
