from enum import Enum
from typing import Annotated

from config import get_config
from db import AUTH_ROBOT_SESSION_DB, AUTH_STORE_SESSION_DB, RedisDependency
from fastapi import Depends, HTTPException, Request


class ClientType(Enum):
    ROBOT = "ROBOT"
    STORE = "STORE"


def auth_request(client_type: ClientType):
    async def func(request: Request, redis_pool: RedisDependency) -> str:
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
            object_id = await redis.get(session_id)

            if object_id is not None:
                redis.expire(session_id, config.AUTH_SESSION_TIMEOUT)
                return object_id.decode("utf-8")
            else:
                raise HTTPException(status_code=401, detail="Invalid credentials")

    return func


StoreAuthRequired = Annotated[str, Depends(auth_request(ClientType.STORE))]
RobotAuthRequired = Annotated[str, Depends(auth_request(ClientType.ROBOT))]
