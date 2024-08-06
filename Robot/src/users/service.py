import datetime

from aiohttp.client import ClientSession

from config import get_config
from users.schemes import User

config = get_config()


async def indentify_face(
        face: str,
        session: ClientSession
) -> User | None:
    async with session.post(
            f"{config.BASE_API_URL}/robot/identification",
            json={
                "image": face
            }
    ) as response:
        if response.status == 404:
            return None

        if response.status != 200:
            raise Exception(f"Unknown server error({response.status}): {await response.text()}")

        return User(**await response.json())


async def get_user_destination(
        session: ClientSession,
        user_id: str,
        train_number: int,
        start_date: datetime.datetime
) -> str | None:
    async with session.post(
            f"{config.BASE_API_URL}/robot/determine_destination",
            json={
                "user_id": user_id,
                "train_number": train_number,
                "start_date": start_date.isoformat()
            }
    ) as response:
        if response.status == 400:
            return None

        if response.status != 200:
            raise Exception(f"Unknown server error({response.status}): {await response.text()}")

        return (await response.json())["id"]
