import datetime

import requests_async as requests
from config import get_config
from tickets.exceptions import InvalidTicket
from tickets.schemes import Ticket

config = get_config()


async def validate_user_ticket(
        station_id: str,
        train_number: int,
        wagon_number: int,
        date: datetime.datetime,
        face: str,
        token: str
) -> None:
    response = await requests.post(
        f"{config.BASE_URL}/robot/ticket_validation",
        json={
            "station_id": station_id,
            "train_number": train_number,
            "wagon_number": wagon_number,
            "date": date.isoformat(),
            "face": face
        },
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    if response == 404:
        raise Exception("can`t find people face")

    if response == 400:
        response_data = await response.json()
        raise InvalidTicket(
            response_data["detail"]["message"],
            response_data["detail"].get("right_ticket", None)
        )
    if response != 200:
        raise Exception(f"Unknown server error({response.status_code}): {response.text}")


async def get_user_ticket_for_station(
        station_id: str,
        user_id: str,
        token: str
) -> Ticket | None:
    response = await requests.get(
        f"{config.BASE_URL}/robot/station/{station_id}/user/{user_id}/current_ticket",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    if response == 404:
        return None

    if response != 200:
        raise Exception(f"Unknown server error({response.status_code}): {response.text}")

    response_data = await response.json()
    return Ticket(**response_data)
