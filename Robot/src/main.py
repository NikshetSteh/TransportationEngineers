import asyncio
import base64
import datetime

from aiohttp.client import ClientSession

from auth.service import auth_admin, is_login, login, new_login
from config import get_config
from info_service.service import (get_destination_attractions,
                                  get_destination_hotels)
from store.schemes import PurchaseCreation
from store.service import (create_purchase, get_store,
                           get_user_recommendation_for_store)
from tickets.service import get_user_ticket_for_station, validate_user_ticket
from users.service import indentify_face


async def main() -> None:
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

        print(f"Authed successfully with token: {session.headers['Authorization']}")

        while True:
            print(
                "Select action:\n"
                "1. Validate user ticket: image_path, station_id, train_number, wagon_number\n"
                "2. Indentify face: image_path\n"
                "3. Get ticket: user_id, station_id\n"
                "4. Get store: store_id\n"
                "5. Get user recommendations for store: user_id, store_id, page=1, size=50\n"
                "6. Make purchase: store_id, data(json)\n"
                "7. Auth admin: admin_card_id\n"
                "8. Get destination attractions: destination_id\n"
                "9. Get destination hotels: destination_id\n"
            )
            action = input(">").split()
            if len(action) < 1:
                continue
            if action[0] == "1":
                if len(action) < 5:
                    print("Invalid count of arguments")
                    continue

                image_path = action[1]
                with open(image_path, "rb") as image_file:
                    face_data = image_file.read()

                try:
                    result = await validate_user_ticket(
                        station_id=action[2],
                        train_number=int(action[3]),
                        wagon_number=int(action[4]),
                        date=datetime.datetime.fromisoformat("2024-07-22T10:53:14.363248+00:00"),
                        face=base64.b64encode(face_data).decode(),
                        session=session
                    )
                except Exception as e:
                    print(e)
                    continue
                print(result.model_dump())
            elif action[0] == "2":
                if len(action) < 2:
                    print("Invalid count of arguments")
                    continue

                image_path = action[1]
                with open(image_path, "rb") as image_file:
                    face_data = image_file.read()

                try:
                    result = await indentify_face(
                        face=base64.b64encode(face_data).decode(),
                        session=session
                    )
                except Exception as e:
                    print(e)
                    continue

                print(result.model_dump_json(indent=4) if result is not None else None)
            elif action[0] == "3":
                if len(action) < 3:
                    print("Invalid count of arguments")
                    continue

                result = await get_user_ticket_for_station(
                    user_id=action[1],
                    station_id=action[2],
                    session=session
                )
                print(result.model_dump_json(indent=4) if result is not None else None)
            elif action[0] == "4":
                if len(action) < 2:
                    print("Invalid count of arguments")
                    continue

                try:
                    result = await get_store(action[1], session)
                except Exception as e:
                    print(e)
                    continue
                print(result.model_dump_json(indent=True) if result is not None else None)
            elif action[0] == "5":
                if len(action) < 3:
                    print("Invalid count of arguments")
                    continue

                try:
                    if len(action) == 3:
                        result = await get_user_recommendation_for_store(
                            user_id=action[1],
                            store_id=action[2],
                            session=session
                        )
                    elif len(action) == 4:
                        result = await get_user_recommendation_for_store(
                            user_id=action[1],
                            store_id=action[2],
                            session=session,
                            page=int(action[3])
                        )
                    elif len(action) == 5:
                        result = await get_user_recommendation_for_store(
                            user_id=action[1],
                            store_id=action[2],
                            session=session,
                            page=int(action[3]),
                            size=int(action[4])
                        )
                except Exception as e:
                    print(e)
                    continue
                print(result.model_dump_json(indent=True))
            elif action[0] == "6":
                if len(action) < 3:
                    print("Invalid count of arguments")
                    continue

                purchase_creation = PurchaseCreation.parse_raw(action[2])
                try:
                    result = await create_purchase(
                        store_id=action[1],
                        user_id=purchase_creation.user_id,
                        items=purchase_creation.items,
                        is_default_ready=purchase_creation.is_default_ready,
                        session=session,
                        additional_data=purchase_creation.additional_data
                    )
                except Exception as e:
                    print(e)
                    continue
                print(result.model_dump_json(indent=True))
            elif action[0] == "7":
                if len(action) < 2:
                    print("Invalid count of arguments")
                    continue

                try:
                    result = await auth_admin(
                        action[1],
                        session
                    )
                except Exception as e:
                    print(e)
                    continue
                print(result.model_dump_json(indent=True))
            elif action[0] == "8":
                if len(action) < 2:
                    print("Invalid count of arguments")
                    continue

                result = await get_destination_attractions(
                    destination_id=action[1],
                    session=session
                )
                print(result.model_dump_json(indent=True))
            elif action[0] == "9":
                if len(action) < 2:
                    print("Invalid count of arguments")
                    continue

                result = await get_destination_hotels(
                    destination_id=action[1],
                    session=session
                )
                print(result.model_dump_json(indent=True))
            else:
                print("Invalid action")
                continue


asyncio.run(main())
