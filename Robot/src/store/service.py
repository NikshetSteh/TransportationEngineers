from aiohttp import ClientSession

from config import get_config
from schemes import Page
from store.schemes import *

config = get_config()


async def get_store(
        store_id: str,
        session: ClientSession
) -> Store | None:
    async with session.get(f"{config.STORE_API_URL}/robot/store/{store_id}") as response:
        if response.status == 404:
            return None

        if response.status != 200:
            raise Exception(f"Unknown server error({response.status}): {await response.text()}")

        return Store.parse_obj(await response.json())


async def get_user_recommendation_for_store(
        user_id: str,
        store_id: str,
        session: ClientSession,
        page: int = 1,
        size: int = 50,
) -> Page[StoreItem]:
    async with session.get(
            f"{config.STORE_API_URL}/robot/store/{store_id}/user/{user_id}/recommendations",
            params={"page": page, "size": size}
    ) as response:
        if response.status == 404:
            raise Exception("User or store not found")
        if response.status != 200:
            raise Exception(f"Unknown server error({response.status}): {await response.text()}")

        return Page[StoreItem].parse_obj(await response.json())


async def create_purchase(
        store_id: str,
        user_id: str,
        items: list[PurchaseItem],
        is_default_ready: bool,
        session: ClientSession,
        additional_data=None,
) -> Purchase:
    if additional_data is None:
        additional_data = {}

    async with session.post(
            f"{config.STORE_API_URL}/robot/store/{store_id}/make_purchase",
            json=PurchaseCreation(
                user_id=user_id,
                items=items,
                is_default_ready=is_default_ready,
                additional_data=additional_data
            ).model_dump()
    ) as response:
        if response.status != 200:
            raise Exception(f"Unknown server error({response.status}): {await response.text()}")

        return Purchase.parse_obj(await response.json())


async def get_train_stores(
        train_number: int,
        session: ClientSession
) -> list[Store]:
    async with session.get(
        f"{config.BASE_API_URL}/robot/train/{train_number}/stores"
    ) as response:
        if response.status != 200:
            raise Exception(f"Unknown server error({response.status}): {await response.text()}")

        data = (await response.json())["items"]

    async with session.post(
            f"{config.STORE_API_URL}/robot/stores/list",
            json={
                "ids": data
            }
    ) as response:
        if response.status != 200:
            raise Exception(f"Unknown server error({response.status}): {await response.text()}")

        return [Store.parse_obj(item) for item in (await response.json())]
