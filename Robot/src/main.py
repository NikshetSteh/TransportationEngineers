import asyncio
import base64
import datetime

from aiohttp.client import ClientSession

from auth.service import is_login, login, new_login
from config import get_config
from tickets.service import validate_user_ticket, get_user_ticket_for_station
from users.service import indentify_face


async def main() -> None:
    async with ClientSession() as session:
        config = get_config()

        if is_login():
            password = input("Enter password: ")
            await login(password, session)
        else:
            engineer_login = input("Enter engineer login: ")
            engineer_password = input("Enter engineer password: ")
            new_password = input("Enter new password: ")

            await new_login(
                engineer_login,
                engineer_password,
                new_password,
                config.ROBOT_MODEL_ID,
                config.ROBOT_MODEL_NAME,
                session
            )

            await login(new_password, session)

        print(f"Authed successfully with token: {session.headers['Authorization']}")

        while True:
            print(
                "Select action:\n"
                "1. Validate user ticket: image_path, station_id, train_number, wagon_number\n"
                "2. Indentify face: image_path\n"
                "3. Get ticket: user_id, station_id\n"
            )
            action = input("Select action: ").split()
            if len(action) < 1:
                continue
            if action[0] == "1":
                if len(action) < 5:
                    print("Invalid count of arguments")
                    continue

                image_path = action[1]
                with open(image_path, "rb") as image_file:
                    face_data = image_file.read()

                result = await validate_user_ticket(
                    station_id=action[2],
                    train_number=int(action[3]),
                    wagon_number=int(action[4]),
                    date=datetime.datetime.fromisoformat("2024-07-22T10:53:14.363248+00:00"),
                    face=base64.b64encode(face_data).decode(),
                    session=session
                )
                print(result.model_dump())
            elif action[0] == "2":
                if len(action) < 2:
                    print("Invalid count of arguments")
                    continue

                image_path = action[1]
                with open(image_path, "rb") as image_file:
                    face_data = image_file.read()

                result = await indentify_face(
                    face=base64.b64encode(face_data).decode(),
                    session=session
                )
                print(result.model_dump())
            elif action[0] == "3":
                if len(action) < 3:
                    print("Invalid count of arguments")
                    continue

                result = await get_user_ticket_for_station(
                    user_id=action[1],
                    station_id=action[2],
                    session=session
                )
                print(result.model_dump() if result is not None else None)


asyncio.run(main())
