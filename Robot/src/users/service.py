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
