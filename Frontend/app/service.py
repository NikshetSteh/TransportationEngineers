from typing import Literal, Annotated

import aiohttp
from fastapi import Request, HTTPException, Depends

from config import get_config
from exceptions import UnauthorizedException

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
            if response.status != 200:
                raise HTTPException(status_code=401, detail="Not authenticated")
            return await response.json()


async def validate_token(
        access_token: str,
) -> None | dict:
    async with aiohttp.ClientSession() as session:
        async with session.post(
                config.user_info_uri,
                headers={
                    "Authorization": f"Bearer {access_token}"
                },
        ) as response:
            if response.status != 200:
                raise UnauthorizedException()

            return await response.json()


async def auth_required(
        request: Request
) -> dict:
    if request.cookies.get("access_token") is None:
        raise UnauthorizedException()

    user_data = await validate_token(
        request.cookies.get("access_token")
    )

    return user_data



AuthRequired = Annotated[dict, Depends(auth_required)]
