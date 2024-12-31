import requests
import base64

from config import BASE_API_URL
from utils import default_print_response, default_print_pagination, input_with_default


def create_user() -> None:
    username = input("Username: ")
    face_path = input_with_default("Face path: ", None)
    if face_path is not None:
        with open(face_path, "rb") as file:
            face = base64.b64encode(file.read()).decode("utf-8")

        response = requests.post(
            f"{BASE_API_URL}/admin/user",
            json={
                "name": username,
                "face": face
            }
        )
    else:
        response = requests.post(
            f"{BASE_API_URL}/admin/user",
            json={
                "name": username
            }
        )
    default_print_response(response)


def get_users() -> None:
    response = requests.get(f"{BASE_API_URL}/admin/users")
    default_print_pagination(response)


def delete_user() -> None:
    user_id = input("User ID: ")
    response = requests.delete(f"{BASE_API_URL}/admin/users/{user_id}")
    default_print_response(response)
