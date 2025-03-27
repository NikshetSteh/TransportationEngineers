from admin.service import create_store, delete_store, get_store, get_stores
from db import DbDependency
from fastapi import APIRouter, Path
from fastapi_pagination import Page, paginate
from robot.schemes import StoreListRequest
from robot.service import get_store_list
from schemes import EmptyResponse
from store.schemes import *

router = APIRouter()


@router.post("/store")
async def create_store_handler(data: StoreCreation, db: DbDependency) -> Store:
    return await create_store(data, db)


@router.get("/stores")
async def get_stores_handler(db: DbDependency) -> Page[Store]:
    return paginate(await get_stores(db))


@router.get("/store/{store_id}")
async def get_store_handler(store_id: str, db: DbDependency) -> Store:
    return await get_store(store_id, db)


@router.delete("/store/{store_id}")
async def delete_store_handler(
    db: DbDependency,
    store_id: str = Path(
        pattern="^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$"
    ),
) -> EmptyResponse:
    await delete_store(store_id, db)
    return EmptyResponse()


@router.get("/ids/stores")
async def get_store_list_handler(
    data: StoreListRequest, db: DbDependency
) -> list[Store]:
    return await get_store_list(data.ids, db)
