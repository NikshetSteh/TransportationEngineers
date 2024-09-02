import base64
import json
import os

import requests
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey

import config
from auth import keys_utility


def save_login_data(
        login_data: dict
) -> None:
    save_data = json.dumps(login_data)

    if not os.path.exists(os.path.dirname(config.LOGIN_FILE_PATH)):
        os.makedirs(config.LOGIN_FILE_PATH)

    with open(config.LOGIN_FILE_PATH, "w") as login_file:
        login_file.write(save_data)


def load_login_data() -> dict:
    with open(config.LOGIN_FILE_PATH, "r") as login_file:
        return json.loads(login_file.read())


def login_by_key(
        private_key: RSAPrivateKey,
        store_id: str
) -> str:
    response = requests.post(
        f"{config.BASE_API_URL}/auth/store/login",
        json={
            "id": store_id
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

    response = requests.post(
        f"{config.BASE_API_URL}/auth/store/login_code",
        json={
            "request_id": login_request_id,
            "data": decrypted_data.decode("utf-8"),
        }
    )
    token = response.json()["token"]
    return f"Bearer {token}"


def new_login(
        engineer_login: str,
        engineer_password: str,
        new_password: str,
        store_id: str
) -> None:
    private_key, public_key = keys_utility.create_keys()
    response = requests.post(
        f"{config.BASE_API_URL}/auth/store/new_login",
        json={
            "login": engineer_login,
            "password": engineer_password,
            "public_key": keys_utility.public_key_to_string(public_key),
            "store_id": store_id
        }
    )

    if response.status_code == 401:
        raise Exception("Invalid credentials")
    if response.status_code != 200:
        raise Exception("Something went wrong. " + response.text)

    store_id = response.json()["id"]
    save_login_data({
        "store_id": store_id
    })
    keys_utility.save_keys(private_key, public_key, new_password)


def is_login() -> bool:
    return os.path.exists(config.LOGIN_FILE_PATH)


def login(
        password: str
) -> str:
    private_key, public_key = keys_utility.try_load_keys(password)
    return login_by_key(private_key, load_login_data()["store_id"])
