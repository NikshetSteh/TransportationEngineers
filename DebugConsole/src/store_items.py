import json
from functools import wraps

import requests

from auth.service import is_login, login, new_login
from config import STORE_API_URL
from utils import default_print_response, input_with_default

session_id: str | None = None


def login_required(
        func
):
    @wraps(func)
    def wrapper(*args, **kwargs):
        global session_id
        if session_id is None:
            if is_login():
                session_id = login("")
            else:
                engineer_login = input("Engineer Login: ")
                engineer_password = input("Engineer Password: ")
                store_id = input("Store ID: ")

                new_login(
                    engineer_login,
                    engineer_password,
                    "",
                    store_id,
                )

                session_id = login("")

        return func(session_id, *args, **kwargs)

    return wrapper


@login_required
def create_store_item(
        session_token: str
) -> None:
    name = input("Name: ")
    description = input("Description: ")
    logo_url = input("Logo URL: ")
    balance = input("Balance: ")
    price_penny = input("Price penny: ")
    category = input("Category: ")

    response = requests.post(
        f"{STORE_API_URL}/store/item",
        json={
            "name": name,
            "description": description,
            "logo_url": logo_url,
            "balance": balance,
            "price_penny": price_penny,
            "category": category
        },
        headers={
            "Authorization": session_token
        }
    )
    default_print_response(response)


@login_required
def get_store_items(
        session_token: str
) -> None:
    response = requests.get(
        f"{STORE_API_URL}/store/items",
        headers={
            "Authorization": session_token
        }
    )
    default_print_response(response)


@login_required
def delete_store_item(
        session_token: str
) -> None:
    item_id = input("Item ID: ")

    response = requests.delete(
        f"{STORE_API_URL}/store/item/{item_id}",
        headers={
            "Authorization": session_token
        }
    )
    default_print_response(response)


@login_required
def update_store_item(
        session_token: str
) -> None:
    item_id = input("Item ID: ")
    name = input("Name: ")
    description = input("Description: ")
    logo_url = input("Logo URL: ")
    balance = input("Balance: ")
    price_penny = input("Price penny: ")
    category = input("Category: ")

    response = requests.put(
        f"{STORE_API_URL}/store/item",
        json={
            "id": item_id,
            "name": name,
            "description": description,
            "logo_url": logo_url,
            "balance": balance,
            "price_penny": price_penny,
            "category": category
        },
        headers={
            "Authorization": session_token
        }
    )

    default_print_response(response)


@login_required
def get_store_tasks(
        session_token: str
) -> None:
    show_ready = input_with_default("Show ready", "0") != "0"
    response = requests.get(
        f"{STORE_API_URL}/store/tasks",
        headers={
            "Authorization": session_token
        },
        params={
            "also_ready_tasks": 1 if show_ready else 0
        }
    )
    default_print_response(response)


@login_required
def mark_task_as_done(
        session_token: str
) -> None:
    task_id = input("Task ID: ")
    response = requests.put(
        f"{STORE_API_URL}/store/task/{task_id}",
        headers={
            "Authorization": session_token
        }
    )
    default_print_response(response)


@login_required
def load_items(
        session_token: str
) -> None:
    file_path = input_with_default("File path", "data/items.json")
    with open(file_path, encoding="utf-8") as file:
        items = json.loads("".join(file.readlines()))

    for item in items:
        response = requests.post(
            f"{STORE_API_URL}/store/item",
            json={
                "name": item["name"],
                "description": item["name"],
                "logo_url": item["logo_url"],
                "balance": item["balance"],
                "price_penny": item["price"],
                "category": item["category"]
            },
            headers={
                "Authorization": session_token
            }
        )
        default_print_response(response)
