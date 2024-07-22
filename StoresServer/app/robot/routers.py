from fastapi import APIRouter

from admin.service import get_store
from db import DbDependency
from store.schemes import Store

router = APIRouter()


@router.get("/store/{store_id}")
async def get_store_handler(
        store_id: str,
        db: DbDependency
) -> Store:
    return await get_store(store_id, db)
