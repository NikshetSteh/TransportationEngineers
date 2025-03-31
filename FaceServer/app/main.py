from face_model import get_model
from fastapi import APIRouter, FastAPI
from routers import router

app = FastAPI()
get_model()

api = APIRouter()

api.include_router(router)

app.include_router(api, prefix="/face_api/v1")
