import requests

from config import STORE_API_URL
from utils import default_print_response, default_print_pagination


def create_store() -> None:
    name = input("Name: ")
    description = input("Description: ")
    logo_url = input("Logo URL: ")
    store_type = input("Store type: ")

    response = requests.post(
        f"{STORE_API_URL}/admin/store",
        json={
            "name": name,
            "description": description,
            "logo_url": logo_url,
            "store_type": store_type
        }
    )
    default_print_response(response)


def get_stores() -> None:
    response = requests.get(f"{STORE_API_URL}/admin/stores")
    default_print_pagination(response)


def get_store() -> None:
    store_id = input("Store ID: ")
    response = requests.get(f"{STORE_API_URL}/admin/store/{store_id}")
    default_print_response(response)


def delete_store() -> None:
    store_id = input("Store ID: ")
    response = requests.delete(f"{STORE_API_URL}/admin/store/{store_id}")
    default_print_response(response)
