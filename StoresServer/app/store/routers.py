from fastapi import APIRouter
from fastapi_pagination import Page, paginate

from db import DbDependency
from store.service import *

router = APIRouter()


@router.get("/{store_id}/items")
async def get_items_handler(
        store_id: str,
        db: DbDependency
) -> Page[StoreItem]:
    return paginate(await get_items(store_id, db.db))


@router.get("/{store_id}/items/{item_id}")
async def get_item_handler(
        store_id: str,
        item_id: str,
        db: DbDependency
) -> StoreItem:
    return await get_item(store_id, item_id, db.db)


@router.post("/{store_id}/item")
async def add_item_handler(
        store_id: str,
        item: StoreItemCreation,
        db: DbDependency
) -> StoreItem:
    return await add_item(store_id, item, db.db)


@router.delete("/{store_id}/item/{item_id}")
async def remove_item_handler(
        store_id: str,
        item_id: str,
        db: DbDependency
) -> None:
    return await remove_item(store_id, item_id, db.db)


@router.put("/{store_id}/item")
async def update_item_handler(
        store_id: str,
        item: StoreItem,
        db: DbDependency
) -> StoreItem:
    return await update_item(store_id, item, db.db)
