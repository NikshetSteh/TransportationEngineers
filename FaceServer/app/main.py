from fastapi import APIRouter, FastAPI

from routers import router

app = FastAPI()

api = APIRouter()

api.include_router(router)

app.include_router(api, prefix="/face_api/v1")
