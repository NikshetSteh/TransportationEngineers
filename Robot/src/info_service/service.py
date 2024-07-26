from aiohttp import ClientSession

from config import get_config
from info_service.schemes import *
from schemes import Page

config = get_config()


async def get_destination_attractions(
        destination_id: str,
        session: ClientSession,
        page: int = 1,
        size: int = 50
) -> Page[Attraction]:
    async with session.get(
            f"{config.BASE_API_URL}/robot/destination/{destination_id}/attractions",
            params={
                "page": page,
                "size": size
            }
    ) as response:
        return Page[Attraction](**(await response.json()))


async def get_destination_hotels(
        destination_id: str,
        session: ClientSession,
        page: int = 1,
        size: int = 50
) -> Page[Hotel]:
    async with session.get(
            f"{config.BASE_API_URL}/robot/destination/{destination_id}/hotels",
            params={
                "page": page,
                "size": size
            }
    ) as response:
        return Page[Hotel](**(await response.json()))
