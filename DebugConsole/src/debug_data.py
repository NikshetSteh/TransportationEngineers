import requests
from utils import input_with_default
import json
from config import BASE_API_URL


def load_debug_data() -> None:
    path_to_hotels = input_with_default("Path to hotels", "data/hotels.json")
    path_to_attractions = input_with_default("Path to attractions", "data/attractions.json")

    with open(path_to_hotels, encoding="utf-8") as file:
        hotels_raw = file.read()
    hotels_data = json.loads(hotels_raw)

    with open(path_to_attractions, encoding="utf-8") as file:
        attractions_raw = file.read()
    attractions_data = json.loads(attractions_raw)

    for hotel in hotels_data:
        response = requests.post(
            f"{BASE_API_URL}/admin/destination/{hotel['destination_id']}/hotel",
            json={
                "name": hotel["name"],
                "description": hotel["description"],
                "logo_url": hotel["logo_url"]
            }
        )
        if response.status_code != 200:
            print("Failed to create hotel:", str(response.json()), str(response.status_code), str(hotel))
            return

    for attraction in attractions_data:
        response = requests.post(
            f"{BASE_API_URL}/admin/destination/{attraction['destination_id']}/attraction",
            json={
                "name": attraction["name"],
                "description": attraction["description"],
                "logo_url": attraction["logo_url"]
            }
        )
        if response.status_code != 200:
            print("Failed to create attraction:", str(response.json()), str(response.status_code), str(attraction))
            return
