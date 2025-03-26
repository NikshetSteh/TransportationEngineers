import base64
from typing import Annotated

import aiohttp
from aiohttp import FormData
from fastapi import Request, Depends, HTTPException

from config import get_config
import logging


logger = logging.getLogger(__name__)


async def keycloak_auth(request: Request) -> str:
    auth_header = request.headers.get("Authorization")
    if auth_header is None or len(auth_header.split()) != 2:
        logger.debug("Try keycloak auth with invalid auth header")
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = auth_header.split()[1]

    config = get_config()
    async with aiohttp.ClientSession() as session:
        form_data = FormData()

        form_data.add_field("token", access_token)

        response = await session.post(
            config.KEYCLOAK_INTROSPECTIVE_ENDPOINT,
            headers={
                "Authorization": f"Basic {
                base64.b64encode(
                    f'{config.CLIENT_ID}:{config.CLIENT_SECRET}'.encode()
                ).decode()
                }"
            },
            data=form_data
        )
        if response.status != 200:
            logger.debug("Try keycloak auth with invalid access token")
            raise HTTPException(status_code=401, detail="Invalid credentials")

        response_json = await response.json()

        if response_json["active"]:
            return response_json["sub"]
        else:
            logger.debug("Try keycloak auth with inactive access token")
            raise HTTPException(status_code=401, detail="Invalid credentials")


KeycloakAuthRequired = Annotated[str, Depends(keycloak_auth)]
