import requests

from config import BASE_API_URL
from utils import default_print_response, default_print_pagination


def create_ticket() -> None:
    user_id = input("User ID: ")
    train_number = int(input("Train number: "))
    wagon_number = int(input("Wagon number: "))
    place_number = int(input("Place number: "))
    station_id = input("Station ID: ")
    date = input("Date: ")

    response = requests.post(
        f"{BASE_API_URL}/admin/ticket",
        json={
            "user_id": user_id,
            "train_number": train_number,
            "wagon_number": wagon_number,
            "place_number": place_number,
            "station_id": station_id,
            "date": date
        }
    )
    default_print_response(response)


def get_tickets() -> None:
    response = requests.get(f"{BASE_API_URL}/admin/tickets")
    default_print_pagination(response)


def delete_ticket() -> None:
    ticket_id = input("Ticket ID: ")
    response = requests.delete(f"{BASE_API_URL}/admin/ticket/{ticket_id}")
    default_print_response(response)

