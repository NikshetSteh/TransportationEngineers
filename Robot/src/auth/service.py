import base64
import json
import os

import requests_async as requests
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey
from requests_async import Response

from auth import keys_utility
from config import get_config

config = get_config()


def save_login_data(
        login_data: dict
) -> None:
    save_data = json.dumps(login_data)

    with open(config.LOGIN_FILE_PATH, "w") as login_file:
        login_file.write(save_data)


def load_login_data() -> dict:
    with open(config.LOGIN_FILE_PATH, "r") as login_file:
        return json.loads(login_file.read())


async def login_by_key(
        private_key: RSAPrivateKey,
        robot_id: str
) -> str:
    response: Response = await requests.post(
        f"ht{config['BASE_URL']}/auth/robot/login",
        json={
            "id": robot_id
        }
    )

    login_code_data = response.json()
    data, login_request_id = login_code_data["data"], login_code_data["request_id"]

    decrypted_data = private_key.decrypt(
        base64.b64decode(data),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    response: Response = await requests.post(
        f"{config['BASE_URL']}/auth/robot/login_code",
        json={
            "request_id": login_request_id,
            "data": decrypted_data.decode("utf-8"),
        }
    )
    return response.json()["token"]


async def new_login(
        engineer_login: str,
        engineer_password: str,
        new_password: str,
        robot_model_id: str,
        robot_model_name: str
) -> None:
    private_key, public_key = keys_utility.create_keys()
    response: Response = await requests.post(
        f"{config['BASE_URL']}/auth/robot/new_login",
        json={
            "login": engineer_login,
            "password": engineer_password,
            "public_key": keys_utility.public_key_to_string(public_key),
            "robot_model_id": robot_model_id,
            "robot_model_name": robot_model_name
        }
    )

    if response.status_code == 401:
        raise Exception("Invalid credentials")
    if response.status_code != 200:
        raise Exception("Something went wrong. " + response.content.decode("utf-8"))

    robot_id = response.json()["id"]
    save_login_data({
        "robot_id": robot_id
    })
    keys_utility.save_keys(private_key, public_key, new_password)


def is_login() -> bool:
    return os.path.exists(config.LOGIN_FILE_PATH)


async def login(
        password: str
) -> str:
    private_key, public_key = keys_utility.try_load_keys(password)
    return await login_by_key(private_key, load_login_data()["robot_id"])