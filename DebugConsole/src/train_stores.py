import requests
from config import BASE_API_URL
from utils import default_print_response, default_print_pagination


def add_train_store() -> None:
    train_number = int(input("Enter train number: "))
    store_id = input("Enter store id: ")

    response = requests.post(f"{BASE_API_URL}/admin/train/{train_number}/store/{store_id}")
    default_print_response(response)


def get_train_stores() -> None:
    train_number = int(input("Enter train number: "))

    response = requests.get(f"{BASE_API_URL}/admin/train/{train_number}/stores")
    default_print_pagination(response)


def delete_train_store() -> None:
    train_number = int(input("Enter train number: "))
    store_id = input("Enter store id: ")

    response = requests.delete(f"{BASE_API_URL}/admin/train/{train_number}/store/{store_id}")
    default_print_response(response)
