from fastapi import APIRouter

from admin.service import get_store
from auth import RobotAuthRequired
from db import DbDependency
from store.schemes import Purchase, PurchaseCreation, Store
from store.service import make_purchase

router = APIRouter()


@router.get("/store/{store_id}")
async def get_store_handler(
        store_id: str,
        db: DbDependency
) -> Store:
    return await get_store(store_id, db)


@router.post("/store/{store_id}/make_purchase")
async def make_purchase_handler(
        store_id: str,
        purchase_data: PurchaseCreation,
        db: DbDependency,
        _: RobotAuthRequired,
) -> Purchase:
    return await make_purchase(
        store_id,
        purchase_data.user_id,
        purchase_data.items,
        purchase_data.is_default_ready,
        db
    )
