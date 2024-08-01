import asyncio
import datetime
import sys
from typing import NoReturn

from aiohttp import ClientSession
from PySide6.QtWidgets import QApplication
from qasync import QEventLoop

from auth.service import is_login, login, new_login
from config import get_config
from fms.fms import FMS
from states.ticket_cheking_state import TicketCheckingState
from utils import async_input


async def process(
        fms: FMS,
        session: ClientSession
) -> NoReturn:
    print(
        "States:",
        "1. Check tickets",
        sep="\n"
    )
    select_new_state = await async_input(
        "Select new state: "
    )

    match select_new_state:
        case "1":
            train_id: int = int(await async_input("Enter train id: "))
            wagon_id: int = int(await async_input("Enter wagon id: "))
            date: datetime.datetime = datetime.datetime.fromisoformat(
                await async_input("Enter date: ")
            )
            station_id: str = await async_input("Enter station id: ")
            fms.change_state(TicketCheckingState(
                station_id,
                train_id,
                wagon_id,
                date,
                session
            ))


async def run_loop(
        session: ClientSession
) -> NoReturn:
    state_machine = FMS()

    while True:
        await process(
            state_machine,
            session
        )


async def main() -> NoReturn:
    async with ClientSession() as session:
        config = get_config()

        if is_login():
            await login("", session)
        else:
            engineer_login = input("Enter engineer login: ")
            engineer_password = input("Enter engineer password: ")

            await new_login(
                engineer_login,
                engineer_password,
                "",
                config.ROBOT_MODEL_ID,
                config.ROBOT_MODEL_NAME,
                session
            )

            await login("", session)

        await run_loop(session)


application = QApplication(sys.argv)
loop = QEventLoop(application)
asyncio.set_event_loop(loop)
loop.run_until_complete(main())
