import base64
import json
import os

from aiohttp.client import ClientSession
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey

from auth import keys_utility
from auth.schemes import *
from config import get_config

config = get_config()


def save_login_data(
        login_data: dict
) -> None:
    save_data = json.dumps(login_data)

    if not os.path.exists(config.LOGIN_FILE_PATH):
        os.mkdir(os.path.dirname(config.LOGIN_FILE_PATH))

    with open(config.LOGIN_FILE_PATH, "w") as login_file:
        login_file.write(save_data)


def load_login_data() -> dict:
    with open(config.LOGIN_FILE_PATH, "r") as login_file:
        return json.loads(login_file.read())


async def login_by_key(
        private_key: RSAPrivateKey,
        robot_id: str,
        session: ClientSession
) -> None:
    async with session.post(
            f"{config.BASE_API_URL}/auth/robot/login",
            json={
                "id": robot_id
            }
    ) as response:
        login_code_data = await response.json()
        data, login_request_id = login_code_data["data"], login_code_data["request_id"]

        try:
            decrypted_data = private_key.decrypt(
                base64.b64decode(data),
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )
        except ValueError:
            raise Exception("Invalid auth")

    async with session.post(
            f"{config.BASE_API_URL}/auth/robot/login_code",
            json={
                "request_id": login_request_id,
                "data": decrypted_data.decode("utf-8"),
            }
    ) as response:
        token = (await response.json())["token"]
        session.headers["Authorization"] = f"Bearer {token}"


async def new_login(
        engineer_login: str,
        engineer_password: str,
        new_password: str,
        robot_model_id: str,
        robot_model_name: str,
        session: ClientSession
) -> None:
    private_key, public_key = keys_utility.create_keys()
    async with session.post(
            f"{config.BASE_API_URL}/auth/robot/new_login",
            json={
                "login": engineer_login,
                "password": engineer_password,
                "public_key": keys_utility.public_key_to_string(public_key),
                "robot_model_id": robot_model_id,
                "robot_model_name": robot_model_name
            }
    ) as response:
        if response.status == 401:
            raise Exception("Invalid credentials")
        if response.status != 200:
            raise Exception("Something went wrong. " + await response.text())

        robot_id = (await response.json())["id"]
        save_login_data({
            "robot_id": robot_id
        })
        keys_utility.save_keys(private_key, public_key, new_password)


def is_login() -> bool:
    return os.path.exists(config.LOGIN_FILE_PATH)


async def login(
        password: str,
        session: ClientSession
) -> None:
    private_key, public_key = keys_utility.try_load_keys(password)
    await login_by_key(private_key, load_login_data()["robot_id"], session)


async def auth_admin(
        key: str,
        session: ClientSession
) -> Admin:
    async with session.post(
            f"{config.BASE_API_URL}/robot/engineer/admin_access",
            json={
                "key": key
            }) as response:
        if response.status == 403:
            raise Exception("Access denied")
        if response.status != 200:
            raise Exception(f"Something went wrong({response.status}): {await response.text()}")

        return Admin(**(await response.json()))
