from typing import Annotated

from config import get_config
from fastapi import Depends
from redis_async import RedisPool
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, AsyncEngine
from sqlalchemy.orm import sessionmaker

db_session_factory: sessionmaker[AsyncSession] | None = None
redit_pool: RedisPool | None = None
engine: AsyncEngine | None = None


async def create_db_connection_factory() -> None:
    global db_session_factory
    global engine

    config = get_config()
    engine = create_async_engine(config.DB_URI, echo=config.SHOW_DB_ECHO)

    # noinspection PyTypeChecker
    factory = sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autoflush=False,
        autocommit=False,
    )

    db_session_factory = factory


async def get_db_connection_factory() -> sessionmaker[AsyncSession]:
    if db_session_factory is None:
        await create_db_connection_factory()

    return db_session_factory


async def close_db_connection_factory() -> None:
    global engine

    if engine is not None:
        await engine.dispose()


async def get_redis() -> RedisPool:
    global redit_pool

    if redit_pool is not None:
        return redit_pool

    config = get_config()
    redit_pool = RedisPool(config.REDIS_URI)
    return redit_pool


DbDependency = Annotated[sessionmaker[AsyncSession], Depends(get_db_connection_factory)]
RedisDependency = Annotated[RedisPool, Depends(get_redis)]

DB = sessionmaker[AsyncSession]

AUTH_ROBOT_REQUEST_DB = 0
AUTH_ROBOT_SESSION_DB = 1
AUTH_STORE_REQUEST_DB = 2
AUTH_STORE_SESSION_DB = 4
