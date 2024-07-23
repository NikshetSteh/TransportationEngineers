import requests

robot_token = "a3457e1b-60dd-4a84-a72d-bead4fa7c992"
user_id = "341e6a5d-b08e-427e-98ef-dc3aeade5b0e"
store_id = "205c2527-4ebc-437e-a61f-95d3a5f428f4"

response = requests.get(f"http://localhost:8040/robot/store/{store_id}/user/{user_id}/recommendations", headers={
    "Authorization": f"Bearer {robot_token}"
})
print(response)
print(response.content.decode())
