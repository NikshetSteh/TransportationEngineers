from fastapi import APIRouter
from fastapi_pagination import Page, paginate

from auth import StoreAuthRequired
from db import DbDependency
from schemes import EmptyResponse
from store.service import *

router = APIRouter()


@router.get("/items")
async def get_items_handler(
        store_id: StoreAuthRequired,
        db: DbDependency
) -> Page[StoreItem]:
    return paginate(await get_items(store_id, db))


@router.get("/item/{item_id}")
async def get_item_handler(
        store_id: StoreAuthRequired,
        item_id: str,
        db: DbDependency
) -> StoreItem:
    return await get_item(store_id, item_id, db)


@router.post("/item")
async def add_item_handler(
        store_id: StoreAuthRequired,
        item: StoreItemCreation,
        db: DbDependency
) -> StoreItem:
    return await add_item(store_id, item, db)


@router.delete("/item/{item_id}")
async def remove_item_handler(
        store_id: StoreAuthRequired,
        item_id: str,
        db: DbDependency
) -> EmptyResponse:
    await remove_item(store_id, item_id, db)

    return EmptyResponse()


@router.put("/item")
async def update_item_handler(
        store_id: StoreAuthRequired,
        item: StoreItem,
        db: DbDependency
) -> StoreItem:
    return await update_item(store_id, item, db)


@router.post("/purchase")
async def make_purchase_handler(
        store_id: StoreAuthRequired,
        purchase_data: PurchaseCreation,
        db: DbDependency
) -> Purchase:
    return await make_purchase(
        store_id,
        purchase_data.user_id,
        purchase_data.items,
        purchase_data.is_default_ready,
        purchase_data.additional_data,
        db
    )


@router.put("/task/{task_id}/ready")
async def mark_as_ready_handler(
        task_id: str,
        db: DbDependency
) -> EmptyResponse:
    await mark_as_ready(task_id, db)
    return EmptyResponse()


@router.get("/tasks")
async def get_tasks_handler(
        store_id: StoreAuthRequired,
        db: DbDependency,
        also_ready_tasks: bool = False
) -> Page[Task]:
    return paginate(await get_tasks(store_id, also_ready_tasks, db))
