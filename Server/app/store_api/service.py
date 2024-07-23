import aiohttp

from config import get_config
from store_api.schemes import *


async def get_store(
    store_id: str,
) -> Store | None:
    config = get_config()

    async with aiohttp.ClientSession() as session:
        url = f"{config.STORE_API}/admin/store/{store_id}"
        async with session.get(url) as response:
            if response.status == 200:
                return Store.parse_raw(await response.text())
            elif response.status == 404:
                return None
            else:
                raise Exception(f"Error: {response.status}, {await response.json()}")
