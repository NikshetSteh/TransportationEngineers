import bcrypt
from db import DB
from fastapi import HTTPException
from keycloak.schemes import ProvidedUser, ProvidedUserCreation, ProvidedUserPatch
from model.user import User as UserModel
from sqlalchemy import select, or_


async def create_user(user_data: ProvidedUserCreation, db: DB) -> ProvidedUser:
    async with db() as session:
        hashed_password = bcrypt.hashpw(
            password=user_data.password.encode(), salt=bcrypt.gensalt()
        )

        user = (await session.execute(
            select(UserModel).where(or_(
                UserModel.username == user_data.username,
                UserModel.email == user_data.email
            ))
        )).scalar()

        if user is not None:
            raise HTTPException(status_code=409, detail="User already exists")

        user = UserModel(
            username=user_data.username,
            name=user_data.full_name,
            email=user_data.email,
            password=hashed_password.decode(),
        )
        session.add(user)
        await session.flush()

        await session.commit()

        return ProvidedUser(
            id=str(user.id),
            username=user.username,
            full_name=user.name,
            email=user.email,
            created_at=int(user.created_at.timestamp()),
        )


async def get_user_by_attribute(attribute: str, value: str, db: DB) -> ProvidedUser | None:
    async with db() as session:
        user: UserModel = (
            await session.execute(
                select(UserModel).where(getattr(UserModel, attribute) == value)
            )
        ).scalar()

    if user is None:
        return None

    return ProvidedUser(
        id=str(user.id),
        username=user.username,
        full_name=user.name,
        email=user.email,
        created_at=int(user.created_at.timestamp()),
    )


async def validate_user_credential(user_id: str, password: str, db: DB) -> bool:
    async with db() as session:
        user = (
            await session.execute(select(UserModel).where(UserModel.id == user_id))
        ).scalar()

    if user is None:
        return False

    if not bcrypt.checkpw(password.encode(), user.password.encode()):
        return False

    return True


async def get_all_users(db: DB) -> list[ProvidedUser]:
    async with db() as session:
        users = (await session.execute(select(UserModel))).scalars()

    return [
        ProvidedUser(
            id=str(user.id),
            username=user.username,
            full_name=user.name,
            email=user.email,
            created_at=int(user.created_at.timestamp()),
        )
        for user in users
    ]


async def update_user(user_id: str, user_data: ProvidedUserPatch, db: DB) -> ProvidedUser:
    async with db() as session:
        user = (
            await session.execute(select(UserModel).where(UserModel.id == user_id))
        ).scalar()

        if user is None:
            raise HTTPException(status_code=404, detail="User not found")

        if user_data.full_name is not None:
            user.name = user_data.full_name

        if user_data.email is not None:
            user.email = user_data.email

        session.add(user)

        await session.commit()

        return ProvidedUser(
            id=str(user.id),
            username=user.username,
            full_name=user.name,
            email=user.email,
            created_at=int(user.created_at.timestamp()),
        )
