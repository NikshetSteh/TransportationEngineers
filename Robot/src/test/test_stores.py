import base64
import json

import requests
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding

from auth import keys_utility

user_id = "76f90fa6-86e1-46ee-b84d-7f5022bd2b24"
engineer_id = "989ad990-2c5f-42ac-b00f-10dc672b4750"
store_id = None
robot_token = "0daa1133-844a-40f1-a912-afaefb4882f0"
store_token = None

item_1 = None
item_2 = None
item_3 = None

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
        "logo_url": "logo_url",
        "store_type": "SHOP"
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

response = requests.post("http://localhost:8040/store/purchase", json={
    "user_id": user_id,
    "items": [
        {
            "item_id": item_3,
            "count": 1
        }
    ],
    "is_default_ready": False,
    "additional_data": {
        "place": 10
    }
}, headers={
    "Authorization": f"Bearer {store_token}"
})
print(response)
print(response.content.decode())

response = requests.get("http://localhost:8040/store/tasks", headers={
    "Authorization": f"Bearer {store_token}"
}, params={
    "also_ready_tasks": 1
})
print(response)
print(response.content.decode())
task_id = json.loads(response.content.decode())["items"][0]["id"]

response = requests.put(f"http://localhost:8040/store/task/{task_id}/ready", headers={
    "Authorization": f"Bearer {store_token}"
})
print(response)
print(response.content.decode())
