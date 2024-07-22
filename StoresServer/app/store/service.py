from fastapi import HTTPException

from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker, selectinload

from model.store import Store as StoreModel
from model.item import StoreItem as StoreItemModel

from store.schemes import *


async def get_item_of_store(
        store_id: str,
        item_id: str,
        db: sessionmaker[AsyncSession]
) -> None | StoreItem:
    async with db() as session:
        stores = (await session.execute(
            select(StoreModel).where(StoreModel.id == store_id).options(selectinload(StoreModel.items))
        )).one_or_none()

        if stores is None:
            raise HTTPException(status_code=404, detail="Store not found")

        items = (await session.execute(
            select(StoreItemModel).where(StoreItemModel.id == item_id)
        )).one_or_none()

        return items if items is None else items[0]


async def add_item(
        store_id: str,
        item: StoreItemCreation,
        db: sessionmaker[AsyncSession]
) -> StoreItem:
    async with db() as session:
        stores = (await session.execute(
            select(StoreModel).where(StoreModel.id == store_id).options(selectinload(StoreModel.items))
        )).one_or_none()

        if stores is None:
            raise HTTPException(status_code=404, detail="Store not found")

        item_model = StoreItemModel(
            store_id=store_id,
            name=item.name,
            description=item.description,
            logo_url=item.logo_url,
            balance=item.balance,
            price_penny=item.price_penny,
            category=item.category
        )

        session.add(item_model)
        await session.commit()

    return StoreItem(
        id=item_model.id,
        store_id=item_model.store_id,
        name=item_model.name,
        description=item_model.description,
        logo_url=item_model.logo_url,
        balance=item_model.balance,
        price_penny=item_model.price_penny,
        category=item_model.category
    )


async def remove_item(
        store_id: str,
        item_id: str,
        db: sessionmaker[AsyncSession]
) -> None:
    async with db() as session:
        item = await get_item_of_store(store_id, item_id, db)
        if item is None:
            raise HTTPException(status_code=404, detail="Item not found")

        await session.execute(
            delete(StoreItemModel).where(StoreItemModel.id == item_id)
        )

        await session.commit()


async def get_item(
        store_id: str,
        item_id: str,
        db: sessionmaker[AsyncSession]
) -> StoreItem:
    item = await get_item_of_store(store_id, item_id, db)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")

    return StoreItem(
        id=item.id,
        store_id=item.store_id,
        name=item.name,
        description=item.description,
        logo_url=item.logo_url,
        balance=item.balance,
        price_penny=item.price_penny,
        category=item.category
    )


async def get_items(
        store_id: str,
        db: sessionmaker[AsyncSession]
) -> list[StoreItem]:
    async with db() as session:
        stores = (await session.execute(
            select(StoreModel).where(StoreModel.id == store_id).options(selectinload(StoreModel.items))
        )).one_or_none()

        if stores is None:
            raise HTTPException(status_code=404, detail="Store not found")

        return list(map(
            lambda x: StoreItem(
                id=x.id,
                store_id=x.store_id,
                name=x.name,
                description=x.description,
                logo_url=x.logo_url,
                balance=x.balance,
                price_penny=x.price_penny,
                category=x.category
            ),
            stores[0].items
        ))


async def update_item(
        store_id: str,
        data: StoreItem,
        db: sessionmaker[AsyncSession]
) -> StoreItem:
    item = await get_item_of_store(store_id, data.id, db)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")

    item.name = data.name
    item.description = data.description
    item.logo_url = data.logo_url
    item.balance = data.balance
    item.price_penny = data.price_penny
    item.category = data.category

    async with db() as session:
        session.add(item)
        await session.commit()

    return item
