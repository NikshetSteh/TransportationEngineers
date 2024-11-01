import asyncio
import datetime
import sys
from typing import NoReturn

from PySide6.QtWidgets import QApplication
from aiohttp import ClientSession
from qasync import QEventLoop

from auth.service import is_login, login, new_login, auth_admin
from config import get_config
from deviant.service import run_deviant_check_loop
from fsm.context import Context
from fsm.fsm import FSM
from hardware.low.port import Port
from hardware.robot import Robot, RobotModule
from states.auth_state import AuthState
from states.ticket_cheking_state import TicketCheckingState
from states.user_menu_state import UserMenuState
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
        "3. Set context var",
        "4. Delete context var",
        "5. Bind train",
        "6. Run deviant loop in background",
        "7. Start robot loop",
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
            var_name = await async_input("Enter var name: ")
            var_value = await async_input("Enter var value: ")
            fsm.context[var_name] = var_value
        case "4":
            var_name = await async_input("Enter var name: ")
            fsm.context.data.pop(var_name)
        case "5":
            train_id: int = int(await async_input("Enter train id: "))
            start_date: datetime.datetime = datetime.datetime.fromisoformat(
                await async_input("Enter date: ")
            )
            fsm.context["train_number"] = train_id
            fsm.context["train_start_date"] = start_date
        case "6":
            # noinspection PyAsyncCall
            asyncio.create_task(run_deviant_check_loop(camera=fsm.context["camera"]))
        case "7":
            com_port = await async_input("Enter com port: ")
            robot_port = Port(
                com_port,
                9600,
                loop=fsm.context["loop"]
            )

            fsm.context["port"] = robot_port

            robot = Robot(
                robot_port
            )

            class KeyModule(RobotModule):
                def check_header(self, header: str) -> bool:
                    return header == "key"

                async def handle(self, header: str, body: str, port: Port):
                    print("Find new key:", body.strip(), "Validating...")
                    try:
                        admin = await auth_admin(body.strip(), fsm.context["session"])
                        print(f"Admin: {admin.id} {admin.login}")
                        await port.write(b"servo 1\n")
                        await asyncio.sleep(5)
                        await port.write(b"servo 0\n")
                    except Exception as e:
                        print(e)
                        await port.write("tone".encode("utf-8"))

            class TelemetryModule(RobotModule):
                def check_header(self, header: str) -> bool:
                    return header == "telemetry" or header == "!telemetry"

                async def handle(self, header: str, body: str, _):
                    if header.startswith("!"):
                        print("Robot can`t get telemetry")

                    humidity, temperature = map(float, body.split(" "))
                    print(f"Robot telemetry: humidity: {humidity}, temperature: {temperature}")

            robot.add_modules(
                KeyModule(),
                TelemetryModule()
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
