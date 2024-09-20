import os

BASE_API_URL = os.environ.get("BASE_API_URL", "http://localhost:8080/base_api/v1")
STORE_API_URL = os.environ.get("STORE_API_URL", "http://localhost:8080/store_api/v1")

KEY_PATH = os.environ.get("KEY_PATH", "private")
LOGIN_FILE_PATH = os.environ.get("LOGIN_FILE_PATH", "private/login_data.dat")