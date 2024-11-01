import datetime

import requests
from config import BASE_API_URL
from utils import default_print_response, default_print_pagination


def add_train_store() -> None:
    store_id = input("Store ID: ")
    train_number = input("Train Number: ")
    train_date = input("Train Date: ")
    train_date = datetime.datetime.fromisoformat(train_date)
    response = requests.post(
        f"{BASE_API_URL}/admin/store/{store_id}/train",
        json={
            "train_number": train_number,
            "train_date": train_date.isoformat()
        }
    )
    default_print_response(response)


def get_train_stores() -> None:
    train_number = int(input("Enter train number: "))
    train_date = input("Enter train date: ")

    response = requests.get(
        f"{BASE_API_URL}/admin/train/stores",
        json={
            "train_number": train_number,
            "train_date": train_date
        }
    )
    default_print_pagination(response)


def delete_train_store() -> None:
    train_number = int(input("Enter train number: "))
    train_date = input("Enter train date: ")
    store_id = input("Enter store id: ")

    response = requests.delete(
        f"{BASE_API_URL}/admin/store/{store_id}/train/unbind",
        json={
            "train_number": train_number,
            "train_date": train_date
        }
    )
    default_print_response(response)
