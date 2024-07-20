from typing import Annotated

import chromadb
from chromadb.api import AsyncClientAPI
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from config import get_config
from model.base import Base

chroma_client: AsyncClientAPI | None = None
db_session_factory: sessionmaker[AsyncSession] | None = None


async def get_chroma_db() -> AsyncClientAPI:
    global chroma_client

    if chroma_client is not None:
        return chroma_client

    config = get_config()
    chroma_client = await chromadb.AsyncHttpClient(
        host=config.CHROMA_DB_HOST,
        port=config.CHROMA_DB_PORT
    )
    return chroma_client


# TODO: Remove!!!
async def update_db_scheme(engine) -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


async def create_db_connection_factory() -> None:
    global db_session_factory

    config = get_config()
    engine = create_async_engine(config.DB_URI, echo=config.SHOW_DB_ECHO)

    await update_db_scheme(engine)

    # noinspection PyTypeChecker
    factory = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False, autoflush=False, autocommit=False
    )

    db_session_factory = factory


async def get_db_connection_factory() -> sessionmaker[AsyncSession]:
    if db_session_factory is None:
        await create_db_connection_factory()

    return db_session_factory


ChromaDependency = Annotated[AsyncClientAPI, Depends(get_chroma_db)]
DbDependency = Annotated[sessionmaker[AsyncSession], Depends(get_db_connection_factory)]
