from fastapi import APIRouter
from fastapi_pagination import Page, paginate

from admin.schemes import *
from admin.service import create_store, delete_store, get_store, get_stores
from db import DbDependency
from schemes import EmptyResponse

router = APIRouter()


@router.post("/store")
async def create_store_handler(
        data: StoreCreation,
        db: DbDependency
) -> Store:
    return await create_store(data, db)


@router.get("/stores")
async def get_stores_handler(
        db: DbDependency
) -> Page[Store]:
    return paginate(await get_stores(db))


@router.get("/store/{store_id}")
async def get_store_handler(
        store_id: str,
        db: DbDependency
) -> Store:
    return await get_store(store_id, db)


@router.delete("/store/{store_id}")
async def delete_store(
        store_id: str,
        db: DbDependency
) -> EmptyResponse:
    await delete_store(store_id, db)
    return EmptyResponse()
