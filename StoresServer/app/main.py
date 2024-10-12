from fastapi import APIRouter, FastAPI
from fastapi_pagination import add_pagination

from admin.routers import router as admin_router
from robot.routers import router as robot_router
from store.routers import router as store_router

app = FastAPI()

api = APIRouter()

api.include_router(admin_router, prefix="/admin")
api.include_router(store_router, prefix="/store")
api.include_router(robot_router, prefix="/robot")

app.include_router(api, prefix="/store_api/v1")

add_pagination(app)
