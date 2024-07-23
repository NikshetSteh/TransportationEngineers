from fastapi import HTTPException
from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload, sessionmaker

from model.history import Purchase as PurchaseModel
from model.item import PurchaseItem as PurchaseItemModel
from model.item import StoreItem as StoreItemModel
from model.store import Store as StoreModel
from model.task import Task as TaskModel
from store.schemes import *


async def get_item_of_store(
        store_id: str,
        item_id: str,
        db: sessionmaker[AsyncSession]
) -> None | StoreItemModel:
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
        id=str(item_model.id),
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
        id=str(item.id),
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
                id=str(x.id),
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

    return StoreItem(
        id=str(item.id),
        store_id=item.store_id,
        name=item.name,
        description=item.description,
        logo_url=item.logo_url,
        balance=item.balance,
        price_penny=item.price_penny,
        category=item.category
    )


async def make_purchase(
        store_id: str,
        user_id: str,
        purchase_items: list[PurchaseItem],
        is_default_ready: bool,
        db: sessionmaker[AsyncSession]
) -> Purchase:
    items_ids = list(map(lambda x: x.item_id, purchase_items))

    async with db() as session:
        stores = (await session.execute(
            select(StoreModel).where(StoreModel.id == store_id).options(selectinload(StoreModel.items))
        )).one_or_none()
        if stores is None:
            raise HTTPException(status_code=404, detail="Store not found")

        items = (await session.execute(
            select(StoreItemModel).where(
                StoreItemModel.id.in_(items_ids),
                StoreItemModel.balance > 0
            )
        )).scalars().all()
        if len(items) != len(items_ids):
            raise HTTPException(status_code=404, detail="Some items not found")

        items = {str(item.id): item for item in items}
        have_bad_items = False
        for item in purchase_items:
            if item.count > items[item.item_id].balance:
                have_bad_items = True
                break

        if have_bad_items:
            raise HTTPException(status_code=400, detail="Not enough items")

        for item in purchase_items:
            await session.execute(
                update(StoreItemModel)
                .where(StoreItemModel.id == item.item_id)
                .values(balance=StoreItemModel.balance - item.count)
            )

        purchase = PurchaseModel(
            store_id=store_id,
            user_id=user_id
        )
        session.add(purchase)
        await session.flush()

        for item in purchase_items:
            session.add(
                PurchaseItemModel(
                    purchase_id=purchase.id,
                    store_item_id=item.item_id,
                    count=item.count
                )
            )

        task = TaskModel(
            purchase_id=purchase.id,
            store_id=store_id,
            user_id=user_id,
            is_ready=is_default_ready
        )
        session.add(task)
        await session.commit()

        return Purchase(
            id=str(purchase.id),
            store_id=purchase.store_id,
            user_id=purchase.user_id,
            items=purchase_items,
            date=purchase.created_at
        )


async def get_tasks(
        store_id: str,
        also_ready_tasks: bool,
        db: sessionmaker[AsyncSession]
) -> list[Task]:
    async with db() as session:
        if also_ready_tasks:
            tasks = (await session.execute(
                select(TaskModel)
                .where(TaskModel.store_id == store_id).options(selectinload(TaskModel.purchase))
            )).scalars().all()
        else:
            tasks = (await session.execute(
                select(TaskModel)
                .where(TaskModel.store_id == store_id, TaskModel.is_ready is False)
                .options(selectinload(TaskModel.purchase))
            )).scalars().all()

        return list(map(
            lambda x: Task(
                id=str(x.id),
                purchase=Purchase(
                    id=str(x.purchase.id),
                    store_id=str(x.purchase.store_id),
                    user_id=str(x.purchase.user_id),
                    items=[PurchaseItem(
                        item_id=str(y.store_item_id),
                        count=y.count
                    ) for y in x.purchase.items],
                    date=x.purchase.created_at
                ),
                store_id=str(x.store_id),
                user_id=str(x.user_id),
                is_ready=x.is_ready,
                date=x.created_at
            ),
            tasks
        ))


async def mark_as_ready(
        task_id: str,
        db: sessionmaker[AsyncSession]
) -> None:
    async with db() as session:
        task = (await session.execute(
            select(TaskModel).where(TaskModel.id == task_id)
        )).scalars().first()
        if task is None:
            raise HTTPException(status_code=404, detail="Task not found")

        task.is_ready = True
        await session.commit()
