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

from auth.client_type import ClientType
from auth.engineer_privileges import (EngineerPrivileges,
                                      engineer_privileges_translations)
from config import get_config
from db import (AUTH_ROBOT_REQUEST_DB, AUTH_ROBOT_SESSION_DB,
                AUTH_STORE_REQUEST_DB, AUTH_STORE_SESSION_DB, RedisDependency)
from model.active_store import ActiveStore
from model.engineer import Engineer
from model.robot import Robot as RobotModel
from redis_async import RedisPool
from robot.schemes import Robot
from store_api.schemes import Store
from store_api.service import get_store


async def create_login_code(
        public_key: str | None,
        redis_db_index: int,
        redis_pool: RedisPool,
        object_id: str | None = None,
) -> tuple[str, str]:
    config = get_config()

    buffer_data = random.choices(config.SYMBOLS_POOL, k=config.AUTH_CODE_LENGTH)
    data = ""
    for i in buffer_data:
        data += i

    if public_key is None:
        encrypted_data_buffer = random.choices(config.SYMBOLS_POOL, k=344)
        encrypted_data = ""
        for i in encrypted_data_buffer:
            encrypted_data += i
        encrypted_data = encrypted_data.encode("utf-8")
    else:
        public_key_text = public_key
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

    if public_key is not None:
        async with redis_pool() as redis:
            await redis.select(redis_db_index)
            await redis.hset(request_id, "data", data)
            await redis.hset(request_id, "object_id", object_id)

    return base64.b64encode(encrypted_data).decode("utf-8"), request_id


async def validate_engineer(
        login: str,
        password: str,
        db: sessionmaker[AsyncSession],
        privilege: int
) -> Engineer:
    async with db() as db_session:
        users = (await db_session.execute(
            db_select(Engineer).where(Engineer.login == login)
        )).one_or_none()

        if users is None:
            raise HTTPException(status_code=401, detail="Invalid credentials")

        user = users[0]

        if not bcrypt.checkpw(password.encode(), user.password.encode()):
            raise HTTPException(status_code=401, detail="Invalid credentials")

        if user.privileges & privilege != privilege:
            raise HTTPException(status_code=403, detail="Insufficient privileges")

    return user


async def create_new_login_for_robot(
        login: str,
        password: str,
        public_key: str,
        robot_model_id: str,
        robot_model_name: str,
        db: sessionmaker[AsyncSession]
) -> Robot:
    async with db() as db_session:
        await validate_engineer(
            login,
            password,
            db,
            engineer_privileges_translations[EngineerPrivileges.ROBOT_LOGIN]
        )

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


async def create_new_login_for_store(
        login: str,
        password: str,
        public_key: str,
        store_id: str,
        db: sessionmaker[AsyncSession]
) -> Store:
    async with db() as db_session:
        await validate_engineer(
            login,
            password,
            db,
            engineer_privileges_translations[EngineerPrivileges.STORE_LOGIN]
        )

        store = await get_store(store_id)

        await db_session.execute(
            db_delete(ActiveStore).where(ActiveStore.id == store_id)
        )

        store_model = ActiveStore(
            id=store.id,
            public_key=public_key
        )

        db_session.add(store_model)
        await db_session.commit()

    return store


async def create_login_code_for_client(
        client_id: str,
        redis_pool: RedisPool,
        db: sessionmaker[AsyncSession],
        client_type: ClientType
) -> tuple[str, str]:
    ClientModelClass = None
    client_db_index = 0
    if client_type == ClientType.ROBOT:
        ClientModelClass = RobotModel
        client_db_index = AUTH_ROBOT_REQUEST_DB
    elif client_type == ClientType.STORE:
        ClientModelClass = ActiveStore
        client_db_index = AUTH_STORE_REQUEST_DB

    async with db() as db_session:
        robots = (await db_session.execute(
            db_select(ClientModelClass).where(ClientModelClass.id == client_id)
        )).one_or_none()
        client: RobotModel | ActiveStore | None = None if robots is None else robots[0]

    return await create_login_code(
        client if client is None else client.public_key,
        client_db_index,
        redis_pool,
        str(client.id) if client is not None else None
    )


async def create_session(
        login_request_id: str,
        login_data: str,
        redis_pool: RedisPool,
        client_type: ClientType
) -> str:
    client_db_request_index = 0
    client_db_session_index = 0
    if client_type == ClientType.ROBOT:
        client_db_request_index = AUTH_ROBOT_REQUEST_DB
        client_db_session_index = AUTH_ROBOT_SESSION_DB
    elif client_type == ClientType.STORE:
        client_db_request_index = AUTH_STORE_REQUEST_DB
        client_db_session_index = AUTH_STORE_SESSION_DB

    config = get_config()

    async with redis_pool() as redis:
        await redis.select(client_db_request_index)
        data = await redis.hget(login_request_id, "data")
        object_id = await redis.hget(login_request_id, "object_id")

    if data is None:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if data.decode("utf-8") != login_data:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    session_id = str(uuid.uuid4())

    async with redis_pool() as redis:
        await redis.select(client_db_request_index)
        await redis.delete(login_request_id)

        await redis.select(client_db_session_index)
        await redis.set(session_id, object_id, ex=config.AUTH_SESSION_TIMEOUT)

    return session_id


def auth_request(client_type: ClientType):
    async def func(
            request: Request,
            redis_pool: RedisDependency
    ) -> str:
        db_index = -1
        if client_type == ClientType.ROBOT:
            db_index = AUTH_ROBOT_SESSION_DB
        elif client_type == ClientType.STORE:
            db_index = AUTH_STORE_SESSION_DB

        auth_header = request.headers.get("Authorization")
        if auth_header is None or len(auth_header.split()) != 2:
            raise HTTPException(status_code=401, detail="Invalid credentials")

        session_id = auth_header.split()[1]

        config = get_config()
        async with redis_pool() as redis:
            await redis.select(db_index)
            robot_id = await redis.get(session_id)

            if robot_id is not None:
                await redis.expire(session_id, config.AUTH_SESSION_TIMEOUT)
                return robot_id
            else:
                raise HTTPException(status_code=401, detail="Invalid credentials")
    return func
