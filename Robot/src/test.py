import asyncio
import datetime
import sys
from typing import NoReturn

from aiohttp import ClientSession
from PySide6.QtWidgets import QApplication
from qasync import QEventLoop

from auth.service import is_login, login, new_login
from config import get_config
from fsm.context import Context
from fsm.fsm import FSM
from states.ticket_cheking_state import TicketCheckingState
from ui.basic_window import BasicWindow
from utils import async_input


async def process(
        fsm: FSM,
        main_window: BasicWindow
) -> NoReturn:
    print(
        "States:",
        "1. Check tickets",
        sep="\n"
    )
    select_new_state = await async_input(
        "Select new state: "
    )

    main_window.show()

    fsm.context["fsm"] = fsm

    match select_new_state:
        case "1":
            train_id: int = int(await async_input("Enter train id: "))
            wagon_id: int = int(await async_input("Enter wagon id: "))
            date: datetime.datetime = datetime.datetime.fromisoformat(
                await async_input("Enter date: ")
            )
            station_id: str = await async_input("Enter station id: ")
            fsm.change_state(TicketCheckingState(
                station_id,
                train_id,
                wagon_id,
                date
            ))


async def run_loop(
        session: ClientSession
) -> NoReturn:
    context = Context()
    state_machine = FSM(context)
    main_window = BasicWindow()

    context["session"] = session
    context["state_machine"] = state_machine
    context["window"] = main_window

    while True:
        await process(
            state_machine,
            main_window
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
