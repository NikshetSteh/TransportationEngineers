import bcrypt
from fastapi import APIRouter, HTTPException
from fastapi_pagination import Page, paginate
from sqlalchemy import delete, select

from admin.schemes import *
from auth.engineer_privileges import engineer_privileges_translations
from db import DbDependency
from face_api.service import delete_face, save_face
from model.engineer import Engineer as EngineerModel
from model.robot import Robot as RobotModel
from model.user import User as UserModel
from robot.schemes import Robot
from schemes import EmptyResponse
from users.schemes import User

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
