from face_api.service import delete_face
from fastapi import HTTPException
from model.keycloak_users import KeycloakUser as KeycloakUserModel
from model.ticket import Ticket as TicketModel
from model.user import User as UserModel
from sqlalchemy import delete, select
from sqlalchemy.orm import sessionmaker
from users.schemes import User


async def create_user(username: str, kid: str, db: sessionmaker):
    async with db() as session:
        users = (
            await session.execute(select(UserModel).where(UserModel.name == username))
        ).one_or_none()

        if users is not None:
            raise HTTPException(status_code=409, detail="User already exists")

        user = UserModel(name=username)
        session.add(user)

        await session.flush()

        print("Start add")
        session.add(KeycloakUserModel(k_id=kid, user_id=user.id))
        print("Finish add")
        await session.commit()
        print("Commit")

    return User(id=str(user.id), name=username)


async def delete_user(user_id: str, db: sessionmaker) -> None:
    async with db() as session:
        user = (
            await session.execute(select(UserModel).where(UserModel.id == user_id))
        ).scalar()

        if user is None:
            raise HTTPException(status_code=404, detail="User not found")

        await session.execute(
            delete(KeycloakUserModel).where(KeycloakUserModel.user_id == user_id)
        )

        await session.execute(delete(TicketModel).where(TicketModel.user_id == user_id))
        await session.execute(delete(UserModel).where(UserModel.id == user_id))
        await session.commit()

        await delete_face(user_id)

        await session.delete(user)
        await session.commit()
