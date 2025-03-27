from admin.service import get_store
from auth import RobotAuthRequired
from db import DbDependency
from fastapi import APIRouter, Path
from fastapi_pagination import Page, paginate
from robot.schemes import StoreListRequest
from robot.service import get_store_list, get_user_recommendations
from store.schemes import Purchase, PurchaseCreation, Store, StoreItem
from store.service import make_purchase

router = APIRouter()


@router.get("/store/{store_id}")
async def get_store_handler(
    db: DbDependency,
    store_id: str = Path(
        pattern="[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}"
    ),
) -> Store:
    return await get_store(store_id, db)


@router.post("/store/{store_id}/make_purchase")
async def make_purchase_handler(
    purchase_data: PurchaseCreation,
    db: DbDependency,
    _: RobotAuthRequired,
    store_id: str = Path(
        pattern="[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}"
    ),
) -> Purchase:
    return await make_purchase(
        store_id,
        purchase_data.user_id,
        purchase_data.items,
        purchase_data.is_default_ready,
        purchase_data.additional_data,
        db,
    )


@router.get("/store/{store_id}/user/{user_id}/recommendations")
async def get_user_recommendations_handler(
    db: DbDependency,
    _: RobotAuthRequired,
    store_id: str = Path(
        pattern="[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}"
    ),
    user_id: str = Path(
        pattern="[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}"
    ),
) -> Page[StoreItem]:
    return paginate(await get_user_recommendations(store_id, user_id, db))


@router.post("/stores/list")
async def get_store_list_handler(
    data: StoreListRequest, db: DbDependency, _: RobotAuthRequired
) -> list[Store]:
    return await get_store_list(data.ids, db)
