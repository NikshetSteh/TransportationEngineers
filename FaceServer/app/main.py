from fastapi import FastAPI, APIRouter

from routers import router

app = FastAPI()

api = APIRouter()

api.include_router(router)

app.include_router(api, prefix="/face_api/v1")
