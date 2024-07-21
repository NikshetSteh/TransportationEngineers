import base64
import random
import uuid

import bcrypt
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from fastapi import HTTPException, Request
from sqlalchemy import delete as db_delete
from sqlalchemy import select as db_select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from config import get_config
from db import AUTH_REQUEST_DB, AUTH_SESSION_DB, RedisDependency
from model.engineer import Engineer
from model.robot import Robot as RobotModel
from redis_async import RedisPool
from robot.schemes import Robot
from auth.engineer_privileges import EngineerPrivileges, engineer_privileges_translations


async def create_new_login(
        login: str,
        password: str,
        public_key: str,
        robot_model_id: str,
        robot_model_name: str,
        db: sessionmaker[AsyncSession]
) -> Robot:
    async with db() as db_session:
        users = (await db_session.execute(
            db_select(Engineer).where(Engineer.login == login)
        )).one_or_none()

        if users is None:
            raise HTTPException(status_code=401, detail="Invalid credentials")

        user = users[0]

        if not bcrypt.checkpw(password.encode(), user.password.encode()):
            raise HTTPException(status_code=401, detail="Invalid credentials")

        if user.privileges & engineer_privileges_translations[EngineerPrivileges.ROBOT_LOGIN] == 0:
            raise HTTPException(status_code=403, detail="Insufficient privileges")

        await db_session.execute(
            db_delete(RobotModel).where(RobotModel.robot_model_id == robot_model_id)
        )

        robot = RobotModel(
            public_key=public_key,
            robot_model_id=robot_model_id,
            robot_model_name=robot_model_name
        )

        db_session.add(robot)
        await db_session.commit()

    return Robot(
        id=str(robot.id),
        robot_model_id=robot.robot_model_id,
        robot_model_name=robot.robot_model_name
    )


async def generate_login_code(
        robot_id: str,
        redis_pool: RedisPool,
        db: sessionmaker[AsyncSession]
) -> tuple[str, str]:
    config = get_config()

    async with db() as db_session:
        robots = (await db_session.execute(
            db_select(RobotModel).where(RobotModel.id == robot_id)
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
            await redis.hset(request_id, "robot_id", robot_id)

    return base64.b64encode(encrypted_data).decode("utf-8"), request_id


async def create_session(
        login_request_id: str,
        login_data: str,
        redis_pool: RedisPool
) -> str:
    config = get_config()

    async with redis_pool() as redis:
        await redis.select(AUTH_REQUEST_DB)
        print(f"request_id: '{login_request_id}'")
        data = await redis.hget(login_request_id, "data")
        robot_id = await redis.hget(login_request_id, "robot_id")

    if data is None:
        print('Can`t read')
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if data.decode("utf-8") != login_data:
        print("Invalid data")
        print(f"'{data}' != '{login_data}'")
        raise HTTPException(status_code=401, detail="Invalid credentials")

    session_id = str(uuid.uuid4())

    async with redis_pool() as redis:
        await redis.select(AUTH_REQUEST_DB)
        await redis.delete(login_request_id)

        await redis.select(AUTH_SESSION_DB)
        await redis.set(session_id, robot_id, ex=config.AUTH_SESSION_TIMEOUT)

    return session_id


async def auth_request(
        request: Request,
        redis_pool: RedisDependency
) -> str:
    auth_header = request.headers.get("Authorization")
    if auth_header is None or len(auth_header.split()) != 2:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    session_id = auth_header.split()[1]

    config = get_config()
    async with redis_pool() as redis:
        await redis.select(AUTH_SESSION_DB)
        robot_id = await redis.get(session_id)

        if robot_id is not None:
            redis.expire(session_id, config.AUTH_SESSION_TIMEOUT)
            return robot_id
        else:
            raise HTTPException(status_code=401, detail="Invalid credentials")
