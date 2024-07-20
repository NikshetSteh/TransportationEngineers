import base64
import random
import uuid

import bcrypt
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from fastapi import APIRouter, HTTPException
from sqlalchemy import delete, select

from auth.schemes import *
from config import get_config
from db import AUTH_REQUEST_DB, AUTH_SESSION_DB, DbDependency, RedisDependency
from model.engineer import Engineer
from model.robot import Robot as RobotModel
from robot.schemes import Robot

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

        await db_session.execute(
            delete(RobotModel).where(RobotModel.robot_model_id == data.robot_model_id)
        )

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


@router.post("/robot/login")
async def login(
        login_request: LoginRequest,
        redis_pool: RedisDependency,
        db: DbDependency
) -> LoginCode:
    config = get_config()

    async with db() as db_session:
        robots = (await db_session.execute(
            select(RobotModel).where(RobotModel.id == login_request.id)
        )).one_or_none()
        robot = None if robots is None else robots[0]

    buffer_data = random.choices(config.SYMBOLS_POOL, k=config.AUTH_CODE_LENGTH)
    data = ""
    for i in buffer_data:
        data += i

    if robots is None:
        encrypted_data_buffer = random.choices(config.SYMBOLS_POOL, k=344)
        encrypted_data = ""
        for i in encrypted_data_buffer:
            encrypted_data += i
    else:
        public_key_text = robot.public_key
        public_key = serialization.load_pem_public_key(
            public_key_text.encode(),
            backend=default_backend()
        )
        encrypted_data = public_key.encrypt(
            data.encode(),
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

    request_id = str(uuid.uuid4())

    if robot is not None:
        async with redis_pool() as redis:
            await redis.select(AUTH_REQUEST_DB)
            await redis.hset(request_id, "data", data)
            await redis.hset(request_id, "robot_id", login_request.id)

    return LoginCode(
        data=base64.b64encode(encrypted_data),
        request_id=request_id
    )


@router.post("/robot/login_code")
async def login_code(
        login_data: LoginCode,
        redis_pool: RedisDependency,
) -> AuthResponse:
    config = get_config()

    async with redis_pool() as redis:
        await redis.select(AUTH_REQUEST_DB)
        print(f"request_id: '{login_data.request_id}'")
        data = await redis.hget(login_data.request_id, "data")
        robot_id = await redis.hget(login_data.request_id, "robot_id")

    if data is None:
        print('Can`t read')
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if data.decode("utf-8") != login_data.data:
        print("Invalid data")
        print(f"'{data}' != '{login_data.data}'")
        raise HTTPException(status_code=401, detail="Invalid credentials")

    session_id = str(uuid.uuid4())

    async with redis_pool() as redis:
        await redis.select(AUTH_REQUEST_DB)
        await redis.delete(login_data.request_id)

        await redis.select(AUTH_SESSION_DB)
        await redis.set(session_id, robot_id, ex=config.AUTH_SESSION_TIMEOUT)

    return AuthResponse(token=session_id)
