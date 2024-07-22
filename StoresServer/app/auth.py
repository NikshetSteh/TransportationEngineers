from typing import Annotated

from fastapi import Depends, HTTPException, Request

from config import get_config
from db import AUTH_STORE_SESSION_DB, RedisDependency


async def auth_request(
        request: Request,
        redis_pool: RedisDependency,
) -> str:
    auth_header = request.headers.get("Authorization")
    if auth_header is None or len(auth_header.split()) != 2:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    session_id = auth_header.split()[1]

    config = get_config()
    async with redis_pool() as redis:
        await redis.select(AUTH_STORE_SESSION_DB)
        object_id = await redis.get(session_id)

        if object_id is not None:
            redis.expire(session_id, config.AUTH_SESSION_TIMEOUT)
            return object_id.decode("utf-8")
        else:
            raise HTTPException(status_code=401, detail="Invalid credentials")


AuthRequired = Annotated[str, Depends(auth_request)]
