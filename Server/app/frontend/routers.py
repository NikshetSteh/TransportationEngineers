from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from config import get_config
from db import DbDependency
from frontend.dependecies import KeycloakAuthRequired
from frontend.schemes import WebhookRequest
from frontend.service import get_user_last_ticket, k_id_to_user_id
from loggers import base_logger
from users.schemes import Ticket
from users.service import create_user, delete_user

logger = base_logger.getChild("frontend")

router = APIRouter()


@router.get("/get_ticket")
async def get_ticket(
        k_id: KeycloakAuthRequired,
        db: DbDependency
) -> Ticket:
    ticket = await get_user_last_ticket(
        k_id,
        db,
    )

    if ticket is None:
        raise HTTPException(status_code=404, detail="Ticket not found")

    return ticket


keycloak_auth = HTTPBasic()


@router.post("/keycloak_listener", status_code=204)
async def keycloak_listener(
        request_data: WebhookRequest,
        db: DbDependency,
        credentials: HTTPBasicCredentials = Depends(keycloak_auth)
) -> None:
    config = get_config()

    if credentials.username != config.KEYCLOAK_WEBHOOK_LOGIN or credentials.password != config.KEYCLOAK_WEBHOOK_PASSWORD:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if request_data.error is None:
        if request_data.type == "REGISTER":
            user = await create_user(
                f"{request_data.details['last_name']} {request_data.details['first_name']}",
                request_data.userId,
                db
            )

            logger.info(
                "New user registered from keycloak: id='{0}', name='{1} {2}'".format(
                    user.id,
                    request_data.details["last_name"],
                    request_data.details["first_name"]
                )
            )
        elif request_data.type == "USER-DELETE":
            await delete_user(
                await k_id_to_user_id(
                    request_data.userId,
                    db
                ),
                db
            )

            logger.info(
                "User deleted from keycloak: id='{0}'".format(
                    request_data.userId
                )
            )

    logger.debug(
        "Keycloak webhook received:\n{0}".format(
            request_data.model_dump_json(indent=4)
        )
    )
