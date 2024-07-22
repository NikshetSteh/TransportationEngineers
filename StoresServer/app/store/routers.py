from fastapi import APIRouter
from fastapi_pagination import Page, paginate

from auth import AuthRequired
from db import DbDependency
from store.service import *

router = APIRouter()


@router.get("/items")
async def get_items_handler(
        store_id: AuthRequired,
        db: DbDependency
) -> Page[StoreItem]:
    return paginate(await get_items(store_id, db))


@router.get("/item/{item_id}")
async def get_item_handler(
        store_id: AuthRequired,
        item_id: str,
        db: DbDependency
) -> StoreItem:
    return await get_item(store_id, item_id, db)


@router.post("/item")
async def add_item_handler(
        store_id: AuthRequired,
        item: StoreItemCreation,
        db: DbDependency
) -> StoreItem:
    return await add_item(store_id, item, db)


@router.delete("/item/{item_id}")
async def remove_item_handler(
        store_id: AuthRequired,
        item_id: str,
        db: DbDependency
) -> None:
    return await remove_item(store_id, item_id, db)


@router.put("/item")
async def update_item_handler(
        store_id: AuthRequired,
        item: StoreItem,
        db: DbDependency
) -> StoreItem:
    return await update_item(store_id, item, db)
