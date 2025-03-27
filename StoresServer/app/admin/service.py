from fastapi import HTTPException
# noinspection PyUnresolvedReferences
from model.item import StoreItem as StoreItemModel
from model.store import Store as StoreModel
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload, sessionmaker
from store.schemes import *


async def create_store(data: StoreCreation, db: sessionmaker[AsyncSession]) -> Store:
    async with db() as session:
        stores = (
            await session.execute(
                select(StoreModel).where(StoreModel.name == data.name)
            )
        ).one_or_none()

        if stores is not None:
            raise HTTPException(
                status_code=409, detail="Store with this name already exists"
            )

        store = StoreModel(**data.dict())
        session.add(store)
        await session.commit()
        await session.refresh(store)

    return Store(
        id=str(store.id),
        name=store.name,
        description=store.description,
        logo_url=store.logo_url,
        store_type=store.store_type,
        items=[],
    )


async def get_stores(db: sessionmaker[AsyncSession]) -> list[Store]:
    async with db() as session:
        stores = (await session.execute(select(StoreModel))).scalars().all()

    return list(
        map(
            lambda x: Store(
                id=str(x.id),
                name=x.name,
                description=x.description,
                logo_url=x.logo_url,
                store_type=x.store_type,
                items=[],
            ),
            stores,
        )
    )


async def get_store(store_id: str, db: sessionmaker[AsyncSession]) -> Store:
    async with db() as session:
        stores = (
            await session.execute(
                select(StoreModel)
                .where(StoreModel.id == store_id)
                .options(selectinload(StoreModel.items))
            )
        ).one_or_none()

        if stores is None:
            raise HTTPException(status_code=404, detail="Store not found")

        store: StoreModel = stores[0]

        return Store(
            id=str(store.id),
            name=store.name,
            description=store.description,
            logo_url=store.logo_url,
            store_type=store.store_type,
            items=list(
                map(
                    lambda x: StoreItem(
                        id=str(x.id),
                        name=x.name,
                        description=x.description,
                        logo_url=x.logo_url,
                        category=x.category,
                        balance=x.balance,
                        price_penny=x.price_penny,
                    ),
                    store.items,
                )
            ),
        )


async def delete_store(store_id: str, db: sessionmaker[AsyncSession]) -> None:
    async with db() as session:
        store = (
            await session.execute(select(StoreModel).where(StoreModel.id == store_id))
        ).one_or_none()

        if store is None:
            raise HTTPException(status_code=404, detail="Store not found")

        await session.execute(delete(StoreModel).where(StoreModel.id == store_id))
        await session.commit()
