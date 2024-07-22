import aiohttp
from fastapi import HTTPException
from fastapi_pagination import Page

from config import get_config
from store_api.schemes import *


async def create_store(
    data: StoreCreation,
) -> Store:
    config = get_config()

    async with aiohttp.ClientSession() as session:
        url = f"{config.STORE_API}/admin/store"
        async with session.post(url, json=data.model_dump()) as response:
            if response.status == 200:
                return await response.json()
            elif response.status == 409:
                raise HTTPException(status_code=409, detail="Store with this name already exists")
            else:
                raise Exception(f"Error: {response.status}, {await response.json()}")


async def get_stores(
        page: int,
        page_size: int
) -> Page[Store]:
    config = get_config()

    async with aiohttp.ClientSession() as session:
        url = f"{config.STORE_API}/admin/stores"
        async with session.get(url, params={
            "page": page,
            "size": page_size
        }) as response:
            if response.status == 200:
                return Page[Store].parse_raw(await response.text())
            else:
                raise Exception(f"Error: {response.status}, {await response.json()}")


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


async def delete_store(
        store_id: str
) -> None:
    config = get_config()

    async with aiohttp.ClientSession() as session:
        url = f"{config.STORE_API}/admin/store/{store_id}"
        async with session.delete(url) as response:
            if response.status == 200:
                return
            elif response.status == 404:
                raise HTTPException(status_code=404, detail="Store not found")
            else:
                raise Exception(f"Error: {response.status}, {await response.json()}")
