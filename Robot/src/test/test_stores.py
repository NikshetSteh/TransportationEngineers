import base64
import json

import requests
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding

from auth import keys_utility

user_id = "735d71d4-6493-4839-9fbe-3ae8ffaa1ed7"
engineer_id = "734dad0b-a261-4620-8ce5-e64744f3a2c5"
store_id = "dcf5ff18-50b3-4b67-a18f-077b1e879ec8"
robot_token = "823c206c-46ca-44b1-bc7a-f5825a6aafef"
store_token = "388ebfb6-4cfd-4258-a719-5b5870291ecb"

item_1 = "9b183a5a-f851-495e-9d2e-ee0f0247f0c7"
item_2 = "58797f3b-bc2f-4e52-8536-f70e1036eba2"
item_3 = "56ebb170-1f0d-49dd-aa1a-6a3960cdf055"

with open("face") as file:
    face = file.read()

if user_id is None:
    response = requests.post("http://localhost:8000/admin/user", json={
        "name": "Tester",
        "face": face
    })
    print(response)
    user_id = json.loads(response.content.decode("utf-8"))["id"]

print("User id:", user_id)

if engineer_id is None:
    response = requests.post("http://localhost:8000/admin/engineer", json={
        "login": "Tester",
        "password": "Test"
    })
    print(response)
    engineer_id = json.loads(response.content.decode("utf-8"))["id"]

print("Engineer id:", engineer_id)

response = requests.put("http://localhost:8000/admin/engineer_privileges", json={
    "id": engineer_id,
    "privileges": [
        "ROBOT_LOGIN",
        "STORE_LOGIN"
    ]
})
print(response)

if store_id is None:
    response = requests.post("http://localhost:8040/admin/store", json={
        "name": "TestStore",
        "description": "Desc",
        "logo_url": "logo_url"
    })
    print(response)
    store_id = json.loads(response.content.decode("utf-8"))["id"]

print("Store id:", store_id)

keys = keys_utility.try_load_keys("test")
private_key, public_key = keys

if robot_token is None:
    response = requests.post(
        "http://localhost:8000/auth/robot/new_login",
        json={
            "login": "Tester",
            "password": "Test",
            "public_key": keys_utility.public_key_to_string(public_key),
            "robot_model_id": "TestBot2",
            "robot_model_name": "Test1"
        }
    )

    if response.status_code == 200:
        print("Successfully created new login.")
        print(response.content.decode("utf-8"))
        # keys_utility.save_keys(private_key, public_key, "test")
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
    robot_token = json.loads(response.content.decode("utf-8"))["token"]

print("Robot token:", robot_token)

# Store
if store_token is None:
    response = requests.post(
        "http://localhost:8000/auth/store/new_login",
        json={
            "login": "Tester",
            "password": "Test",
            "public_key": keys_utility.public_key_to_string(public_key),
            "store_id": store_id
        }
    )

    if response.status_code == 200:
        print("Successfully created new login.")
        print(response.content.decode("utf-8"))
        # keys_utility.save_keys(private_key, public_key, "test")
    else:
        print(response.content.decode("utf-8"))
        print("Something went wrong. Try again.")
        raise Exception("Something went wrong. Try again.")

    response = requests.post("http://localhost:8000/auth/store/login", json={
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

    response = requests.post("http://localhost:8000/auth/store/login_code", json={
        "request_id": request_id,
        "data": decrypted_data.decode("utf-8"),
    })
    print(response)
    print(response.content.decode("utf-8"))
    store_token = json.loads(response.content.decode("utf-8"))["token"]

print("Store token:", store_token)

if item_1 is None:
    response = requests.post("http://localhost:8040/store/item", json={
        "name": "Test Item1",
        "description": "This is test item",
        "logo_url": "url for item 1",
        "balance": 10,
        "price_penny": 100 * 100,
        "category": "Test items",
    }, headers={
        "Authorization": f"Bearer {store_token}"
    })
    print(response)
    print(response.content.decode("utf-8"))
    item_1 = json.loads(response.content.decode("utf-8"))["id"]

if item_2 is None:
    response = requests.post("http://localhost:8040/store/item", json={
        "name": "Test Item2",
        "description": "This is test item",
        "logo_url": "url for item 2",
        "balance": 10,
        "price_penny": 100 * 100,
        "category": "Test items",
    }, headers={
        "Authorization": f"Bearer {store_token}"
    })
    print(response)
    print(response.content.decode("utf-8"))
    item_2 = json.loads(response.content.decode("utf-8"))["id"]

if item_3 is None:
    response = requests.post("http://localhost:8040/store/item", json={
        "name": "Test Item3",
        "description": "This is test item",
        "logo_url": "url for item 3",
        "balance": 10,
        "price_penny": 100 * 100,
        "category": "Test items",
    }, headers={
        "Authorization": f"Bearer {store_token}"
    })
    print(response)
    print(response.content.decode("utf-8"))
    item_3 = json.loads(response.content.decode("utf-8"))["id"]

response = requests.get("http://localhost:8040/store/items", headers={
    "Authorization": f"Bearer {store_token}"
})
print(response)
print(response.content.decode("utf-8"))

response = requests.delete(f"http://localhost:8040/store/item/{item_1}", headers={
    "Authorization": f"Bearer {store_token}"
})
print(response)

response = requests.put("http://localhost:8040/store/item", json={
    "id": item_2,
    "name": "TTTTTT",
    "description": "This is test item",
    "logo_url": "url for item 3",
    "balance": 10,
    "price_penny": 100 * 100,
    "category": "Test items",
}, headers={
    "Authorization": f"Bearer {store_token}"
})
print("Update results")
print(response)
print(response.content.decode("utf-8"))

response = requests.get(f"http://localhost:8040/store/item/{item_3}", headers={
    "Authorization": f"Bearer {store_token}"
})
print(response)
print(response.content.decode("utf-8"))

response = requests.get("http://localhost:8040/store/items", headers={
    "Authorization": f"Bearer {store_token}"
})
print(response)
print(response.content.decode("utf-8"))
