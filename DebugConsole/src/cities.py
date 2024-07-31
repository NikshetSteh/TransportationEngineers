import requests

from config import BASE_API_URL
from utils import default_print_response, default_print_pagination


def create_hotel() -> None:
    name = input("Name: ")
    description = input("Description: ")
    logo_url = input("Logo URL: ")
    destination_id = input("Destination ID: ")

    response = requests.post(
        f"{BASE_API_URL}/admin/destination/{destination_id}/hotel",
        json={
            "name": name,
            "description": description,
            "logo_url": logo_url
        }
    )
    default_print_response(response)


def create_attraction() -> None:
    name = input("Name: ")
    description = input("Description: ")
    logo_url = input("Logo URL: ")
    destination_id = input("Destination ID: ")

    response = requests.post(
        f"{BASE_API_URL}/admin/destination/{destination_id}/attraction",
        json={
            "name": name,
            "description": description,
            "logo_url": logo_url
        }
    )
    default_print_response(response)


def get_hotels() -> None:
    destination_id = input("Destination ID: ")
    response = requests.get(f"{BASE_API_URL}/admin/destination/{destination_id}/hotels")
    default_print_pagination(response)


def get_attractions() -> None:
    destination_id = input("Destination ID: ")
    response = requests.get(f"{BASE_API_URL}/admin/destination/{destination_id}/attractions")
    default_print_pagination(response)


def delete_hotel() -> None:
    hotel_id = input("Hotel ID: ")
    response = requests.delete(f"{BASE_API_URL}/admin/destination_info/hotel/{hotel_id}")
    default_print_response(response)


def delete_attraction() -> None:
    attraction_id = input("Attraction ID: ")
    response = requests.delete(f"{BASE_API_URL}/admin/destination_info/attraction/{attraction_id}")
    default_print_response(response)
