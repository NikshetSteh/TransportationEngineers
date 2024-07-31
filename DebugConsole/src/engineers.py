from enum import Enum

import requests

from config import BASE_API_URL
from utils import default_print_response, default_print_pagination, input_with_default


class EngineerPrivileges(Enum):
    ROBOT_LOGIN = "ROBOT_LOGIN"
    STORE_LOGIN = "STORE_LOGIN"
    ROBOT_ADMIN = "ROBOT_ADMIN"


def create_engineer() -> None:
    login = input("Login: ")
    password = input("Password: ")

    response = requests.post(
        f"{BASE_API_URL}/admin/engineer",
        json={
            "login": login,
            "password": password
        }
    )
    default_print_response(response)


def get_engineers() -> None:
    response = requests.get(f"{BASE_API_URL}/admin/engineers")
    default_print_pagination(response)


def set_engineer_privileges() -> None:
    engineer_id = input("Engineer ID: ")
    privileges = []
    for privilege in EngineerPrivileges:
        buffer = input_with_default(f"{privilege.name}", None)
        if buffer is not None:
            privileges.append(privilege.name)

    response = requests.put(
        f"{BASE_API_URL}/admin/engineer_privileges",
        json={
            "id": engineer_id,
            "privileges": privileges
        }
    )
    default_print_response(response)


def delete_engineer() -> None:
    engineer_id = input("Engineer ID: ")
    response = requests.delete(f"{BASE_API_URL}/admin/engineers/{engineer_id}")
    default_print_response(response)


def set_engineer_cart_id() -> None:
    engineer_id = input("Engineer ID: ")
    card_key = input("Card key: ")

    response = requests.put(
        f"{BASE_API_URL}/admin/engineer/{engineer_id}/auth_card",
        json={
            "key": card_key
        }
    )
    default_print_response(response)
