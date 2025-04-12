from typing import Annotated

import aiohttp
from fastapi import Depends, HTTPException, Request

from config import get_config
from keycloak.schemes import keycloak_id_strip
from loggers import base_logger

auth_logger = base_logger.getChild("auth")


async def keycloak_auth(request: Request) -> str:
    auth_header = request.headers.get("Authorization")
    if auth_header is None or len(auth_header.split()) != 2:
        auth_logger.debug("Try keycloak auth with invalid auth header")
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = auth_header.split()[1]

    config = get_config()
    async with aiohttp.ClientSession() as session:
        response = await session.post(
            config.KEYCLOAK_INTROSPECTIVE_ENDPOINT,
            headers={
                "Authorization": f"Bearer {access_token}"
            },
        )

        if response.status != 200:
            auth_logger.debug("Try keycloak auth with invalid access token")
            raise HTTPException(status_code=401, detail="Invalid credentials")

        response_json = await response.json()

        return keycloak_id_strip(response_json["sub"])


KeycloakAuthRequired = Annotated[str, Depends(keycloak_auth)]
