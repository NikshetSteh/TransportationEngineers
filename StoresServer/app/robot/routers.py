from fastapi import APIRouter
from fastapi_pagination import Page, paginate

from admin.service import get_store
from auth import RobotAuthRequired
from db import DbDependency
from store.schemes import Purchase, PurchaseCreation, Store, StoreItem
from store.service import make_purchase
from robot.service import get_user_recommendations

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
        purchase_data.additional_data,
        db
    )


@router.get("/store/{store_id}/user/{user_id}/recommendations")
async def get_user_recommendations_handler(
        store_id: str,
        user_id: str,
        db: DbDependency,
        _: RobotAuthRequired
) -> Page[StoreItem]:
    return paginate(
        await get_user_recommendations(
            store_id,
            user_id,
            db
        )
    )
