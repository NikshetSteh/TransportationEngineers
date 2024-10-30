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
from hardware.low.port import Port
from hardware.robot import Robot, RobotModule
from states.auth_state import AuthState
from states.destination_info_state import DestinationInfoState
from states.ticket_cheking_state import TicketCheckingState
from states.user_menu_state import UserMenuState
from ui.basic_window import BasicWindow
from utils import async_input
from video.camera import Camera


async def hardware_loop(
        port: Port
) -> NoReturn:
    async with port:
        print("Check")
        while True:
            data = await port.read()
            print(data)
            await asyncio.sleep(0.1)


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
        "8. Get stores of train",
        "9. Connect by com",
        "10. Run hardware loop",
        "11. Start robot loop",
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
            train_number = await async_input("Enter train number: ")
            train_date = await async_input("Enter train date: ")
            response = await fsm.context["session"].get(
                f"{get_config().BASE_API_URL}/robot/train/stores",
                json={
                    "train_number": train_number,
                    "train_date": train_date
                }
            )
            print(await response.json())
        case "9":
            com_port = await async_input("Enter com port: ")
            port = Port(
                com_port,
                9600,
                loop=fsm.context["loop"]
            )
            fsm.context["port"] = port
        case "10":
            # noinspection PyAsyncCall
            asyncio.create_task(hardware_loop(fsm.context["port"]))
        case "11":
            com_port = await async_input("Enter com port: ")
            port = Port(
                com_port,
                9600,
                loop=fsm.context["loop"]
            )

            fsm.context["port"] = port

            robot = Robot(
                port
            )

            class TestModule(RobotModule):
                def check_header(self, header: str) -> bool:
                    return header == "key"

                async def handle(self, header: str, body: str):
                    print("Find new key:", body)

            robot.add_module(
                TestModule()
            )

            # noinspection PyAsyncCall
            asyncio.create_task(robot.loop(fsm))
        case _:
            print("Invalid state")


async def run_loop(
        session: ClientSession,
        camera: Camera,
        global_loop
) -> NoReturn:
    context = Context()
    state_machine = FSM(context)
    main_window = BasicWindow()

    context["session"] = session
    context["state_machine"] = state_machine
    context["window"] = main_window
    context["camera"] = camera
    context["loop"] = global_loop

    while True:
        await process(
            state_machine,
            main_window
        )


async def main(global_loop) -> NoReturn:
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
            await run_loop(session, camera, global_loop)


if __name__ == "__main__":
    application = QApplication(sys.argv)
    loop = QEventLoop(application)
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main(loop))
