import aiohttp
from fastapi import HTTPException

from config import get_config


async def save_face(
        image: str,
        user_id: str
) -> None:
    config = get_config()

    async with aiohttp.ClientSession() as session:
        url = f"{config.FACE_API}/face"
        async with session.post(url, json={
            "image": image,
            "user_id": user_id
        }) as response:
            if response.status == 200:
                return
            elif response.status == 409:
                raise HTTPException(status_code=409, detail="Face already exists")
            else:
                raise Exception(f"Error: {response.status}, {await response.json()}")


async def search_face(
        image: str
) -> str | None:
    config = get_config()

    async with aiohttp.ClientSession() as session:
        url = f"{config.FACE_API}/search"
        async with session.post(url, json={
            "image": image
        }) as response:
            if response.status == 200:
                return (await response.json())["user_id"]
            elif response.status == 404:
                return None
            else:
                raise HTTPException(status_code=response.status, detail=(await response.json())["detail"])


async def delete_face(
        user_id: str
) -> None:
    config = get_config()

    async with aiohttp.ClientSession() as session:
        url = f"{config.FACE_API}/face/{user_id}"
        async with session.delete(url) as response:
            if response.status == 200:
                return
            else:
                raise Exception(f"Error: {response.status}, {await response.json()}")
