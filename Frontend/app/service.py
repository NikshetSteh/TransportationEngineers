import aiohttp
from config import get_config
from typing import Literal

config = get_config()


async def get_token(
        data: str,
        grant_type: Literal["authorization_code", "refresh_token"],
        redirect_uri: str
) -> tuple[str, int, str, int]:
    async with aiohttp.ClientSession() as session:
        async with session.post(
                config.auth_token_uri,
                data={
                    "client_id": config.client_id,
                    "client_secret": config.client_secret,
                    "grant_type": "authorization_code",
                    "code": data,
                    "redirect_uri": redirect_uri
                } if grant_type == "authorization_code" else {
                    "client_id": config.client_id,
                    "client_secret": config.client_secret,
                    "grant_type": "refresh_token",
                    "refresh_token": data,
                    "redirect_uri": redirect_uri
                },
        ) as response:
            data = await response.json()

            print(data, response.status)

            if response.status != 200:
                raise Exception("Something went wrong: " + data["error"] + "; " + data["error_description"])

            return data["access_token"], data["expires_in"], data["refresh_token"], data["refresh_expires_in"]


async def get_user_data(
        access_token: str,
) -> dict:
    async with aiohttp.ClientSession() as session:
        async with session.post(
                config.user_info_uri,
                headers={
                    "Authorization": f"Bearer {access_token}"
                }
        ) as response:
            return await response.json()
