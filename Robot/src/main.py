import asyncio
import datetime
import sys
from typing import NoReturn

from aiohttp import ClientSession
from PySide6.QtWidgets import QApplication
from qasync import QEventLoop

from auth.service import is_login, login, new_login
from config import get_config
from deviant.service import run_deviant_check_loop
from fsm.context import Context
from fsm.fsm import FSM
from states.auth_state import AuthState
from states.destination_info_state import DestinationInfoState
from states.store_category_selection_state import StoreCategorySelectionState
from states.store_item_state import StoreItemState
from states.ticket_cheking_state import TicketCheckingState
from states.user_menu_state import UserMenuState
from store.schemes import StoreItem
from ui.basic_window import BasicWindow
from utils import async_input
from video.camera import Camera


async def process(
        fsm: FSM,
        main_window: BasicWindow,
) -> NoReturn:
    print(
        "States:",
        "1. Check tickets",
        "2. User auth",
        "3. Destination info",
        "4. Set context var",
        "5. Delete context var",
        "6. Bind train",
        "7. Run deviant loop",
        "8. Store category selection",
        "9. Store item view",
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
        case "2":
            fsm.change_state(
                AuthState(
                    UserMenuState
                )
            )
        case "3":
            destination = await async_input("Enter destination: ")
            fsm.change_state(
                DestinationInfoState(
                    destination
                )
            )
        case "4":
            var_name = await async_input("Enter var name: ")
            var_value = await async_input("Enter var value: ")
            fsm.context[var_name] = var_value
        case "5":
            var_name = await async_input("Enter var name: ")
            fsm.context.data.pop(var_name)
        case "6":
            train_id: int = int(await async_input("Enter train id: "))
            start_date: datetime.datetime = datetime.datetime.fromisoformat(
                await async_input("Enter date: ")
            )
            fsm.context["train_number"] = train_id
            fsm.context["train_start_date"] = start_date
        case "7":
            # noinspection PyAsyncCall
            asyncio.create_task(run_deviant_check_loop(camera=fsm.context["camera"]))
        case "8":
            store_id = await async_input("Enter store id: ")
            fsm.change_state(
                StoreCategorySelectionState(
                    store_id
                )
            )
        case "9":
            item_id = await async_input("Enter item id: ")
            item_name = await async_input("Enter item name: ")
            item_description = await async_input("Enter item description: ")
            item_price_penny = int(await async_input("Enter item price: "))
            item_balance = int(await async_input("Enter item balance: "))
            item_category = await async_input("Enter item category: ")
            item_logo_url = await async_input("Enter item logo url: ")
            fsm.change_state(
                (
                    StoreItemState(
                        StoreItem(
                            id=item_id,
                            name=item_name,
                            description=item_description,
                            price_penny=item_price_penny,
                            balance=item_balance,
                            category=item_category,
                            logo_url=item_logo_url
                        )
                    )
                )
            )
        case _:
            print("Invalid state")


async def run_loop(
        session: ClientSession,
        camera: Camera
) -> NoReturn:
    context = Context()
    state_machine = FSM(context)
    main_window = BasicWindow()

    context["session"] = session
    context["state_machine"] = state_machine
    context["window"] = main_window
    context["camera"] = camera

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

        with Camera() as camera:
            await run_loop(session, camera)


if __name__ == "__main__":
    application = QApplication(sys.argv)
    loop = QEventLoop(application)
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main())
