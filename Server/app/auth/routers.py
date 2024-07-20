from fastapi import APIRouter
from auth.schemes import *
from robot.schemes import Robot
from db import DbDependency
import bcrypt
from model.engineer import Engineer
from model.robot import Robot as RobotModel
from sqlalchemy import select
from fastapi import HTTPException

router = APIRouter()


@router.post("/robot/new_login")
async def new_login(
        data: NewLogin,
        db: DbDependency
):
    async with db() as db_session:
        users = (await db_session.execute(
            select(Engineer).where(Engineer.login == data.login)
        )).one_or_none()

        if users is None:
            raise HTTPException(status_code=401, detail="Invalid credentials")

        user = users[0]

        if not bcrypt.checkpw(data.password.encode(), user.password.encode()):
            raise HTTPException(status_code=401, detail="Invalid credentials")

        robot = RobotModel(
            public_key=data.public_key,
            robot_model_id=data.robot_model_id,
            robot_model_name=data.robot_model_name
        )

        db_session.add(robot)
        await db_session.commit()

    return Robot(
        id=str(robot.id),
        robot_model_id=robot.robot_model_id,
        robot_model_name=robot.robot_model_name
    )
