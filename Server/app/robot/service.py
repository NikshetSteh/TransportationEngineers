from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from face_api.service import search_face
from model.user import User as UserModel
from users.schemes import User


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
