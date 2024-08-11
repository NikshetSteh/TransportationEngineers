import datetime

from aiohttp.client import ClientSession

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
        session: ClientSession
) -> Ticket:
    async with session.post(
        f"{config.BASE_API_URL}/robot/ticket_validation",
        json={
            "station_id": station_id,
            "train_number": train_number,
            "wagon_number": wagon_number,
            "date": date.isoformat(),
            "face": face
        }
    ) as response:
        if response.status == 404:
            raise Exception("can`t find people face")

        if response.status == 400:
            response_data = await response.json()
            if isinstance(response_data["detail"], str):
                raise InvalidTicket(
                    response_data["detail"],
                    None
                )
            raise InvalidTicket(
                response_data["detail"]["message"],
                Ticket.parse_obj(response_data["detail"]["right_ticket"])
                if "right_ticket" in response_data["detail"] else None
            )
        if response.status != 200:
            raise Exception(f"Unknown server error({response.status}): {await response.text()}")

        return Ticket.parse_obj(await response.json())


async def get_user_ticket_for_station(
        station_id: str,
        user_id: str,
        session: ClientSession
) -> Ticket | None:
    async with session.get(
        f"{config.BASE_API_URL}/robot/station/{station_id}/user/{user_id}/current_ticket"
    ) as response:
        if response.status == 404:
            return None

        if response.status != 200:
            raise Exception(f"Unknown server error({response.status}): {await response.text()}")

        response_data = await response.json()
        return Ticket(**response_data)
