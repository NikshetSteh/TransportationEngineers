from typing import Literal, Annotated

import aiohttp
from fastapi import Request, HTTPException, Depends
from fastapi.responses import RedirectResponse

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
                config.AUTH_TOKEN_URI,
                data={
                    "client_id": config.CLIENT_ID,
                    "client_secret": config.CLIENT_SECRET,
                    "grant_type": "authorization_code",
                    "code": data,
                    "redirect_uri": redirect_uri
                } if grant_type == "authorization_code" else {
                    "client_id": config.CLIENT_ID,
                    "client_secret": config.CLIENT_SECRET,
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
                config.USER_INFO_URI,
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
                config.USER_INFO_URI,
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

    user_data["access_token"] = request.cookies.get("access_token")

    return user_data


async def auth_exception_handler(request: Request, exc: UnauthorizedException) -> RedirectResponse:
    return RedirectResponse("/login?redirect=" + request.url.path)


AuthRequired = Annotated[dict, Depends(auth_required)]
