import base64
import json

import requests
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding

from auth import keys_utility

if keys_utility.is_keys_exist():
    while True:
        try:
            keys = keys_utility.try_load_keys(input("Enter password: "))
            if keys is not None:
                private_key, public_key = keys
                break
            else:
                print("Something went wrong. Try again.")
        except ValueError as e:
            print("Invalid password")
else:
    login = input("Login: ")
    password = input("Password: ")
    keys_password = input("Keys password: ")

    private_key, public_key = keys_utility.create_keys()

    response = requests.post(
        "http://localhost:8000/auth/robot/new_login",
        json={
            "login": login,
            "password": password,
            "public_key": keys_utility.public_key_to_string(public_key),
            "robot_model_id": "TestBot2",
            "robot_model_name": "Test1"
        }
    )

    if response.status_code == 200:
        print("Successfully created new login.")
        print(response.content.decode("utf-8"))
        keys_utility.save_keys(private_key, public_key, keys_password)
    else:
        print(response.content.decode("utf-8"))
        print("Something went wrong. Try again.")
        raise Exception("Something went wrong. Try again.")

    response = requests.post("http://localhost:8000/auth/robot/login", json={
        "id": json.loads(response.content.decode("utf-8"))["id"],
    })
    print(response)
    print(response.content.decode("utf-8"))

    response_json = json.loads(response.content.decode("utf-8"))
    data, request_id = response_json["data"], response_json["request_id"]

    decrypted_data = private_key.decrypt(
        base64.b64decode(data),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    print(decrypted_data)
    print(decrypted_data.decode("utf-8"))

    response = requests.post("http://localhost:8000/auth/robot/login_code", json={
        "request_id": request_id,
        "data": decrypted_data.decode("utf-8"),
    })
    print(response)
    print(response.content.decode("utf-8"))
