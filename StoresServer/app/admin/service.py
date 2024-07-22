from fastapi import HTTPException
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload, sessionmaker

from admin.schemes import *
# noinspection PyUnresolvedReferences
from model.item import StoreItem as StoreItemModel
from model.store import Store as StoreModel


async def create_store(
        data: StoreCreation,
        db: sessionmaker[AsyncSession]
) -> Store:
    async with db() as session:
        stores = (await session.execute(
            select(StoreModel).where(StoreModel.name == data.name)
        )).one_or_none()

        if stores is not None:
            raise HTTPException(status_code=409, detail="Store with this name already exists")

        store = StoreModel(**data.dict())
        session.add(store)
        await session.commit()
        await session.refresh(store)

    return Store(
        id=str(store.id),
        name=store.name,
        description=store.description,
        logo_url=store.logo_url,
        items=[]
    )


async def get_stores(
        db: sessionmaker[AsyncSession]
) -> list[Store]:
    async with db() as session:
        stores = (await session.execute(select(StoreModel))).scalars().all()

    return list(map(
        lambda x: Store(
            id=str(x.id),
            name=x.name,
            description=x.description,
            logo_url=x.logo_url,
            items=[]
        ),
        stores
    ))


async def get_store(
        store_id: str,
        db: sessionmaker[AsyncSession]
) -> Store:
    async with db() as session:
        stores = (await session.execute(
            select(StoreModel).where(StoreModel.id == store_id).options(
                selectinload(StoreModel.items)
            )
        )).one_or_none()

        if stores is None:
            raise HTTPException(status_code=404, detail="Store not found")

        store = stores[0]

        return Store(
            id=str(store.id),
            name=store.name,
            description=store.description,
            logo_url=store.logo_url,
            items=list(map(
                lambda x: StoreItem(
                    id=str(x.id),
                    name=x.name,
                    description=x.description,
                    logo_url=x.logo_url,
                    category=x.category
                ),
                store.items
            ))
        )


async def delete_store(
        store_id: str,
        db: sessionmaker[AsyncSession]
) -> None:
    async with db() as session:
        store = (await session.execute(
            select(StoreModel).where(StoreModel.id == store_id)
        )).one_or_none()

        if store is None:
            raise HTTPException(status_code=404, detail="Store not found")

        await session.execute(
            delete(StoreModel).where(StoreModel.id == store_id)
        )
        await session.commit()
