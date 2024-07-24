from aiohttp import ClientSession
from store.schemes import Store
from config import get_config

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
