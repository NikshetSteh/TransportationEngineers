from fastapi import FastAPI
from fastapi_pagination import add_pagination

from admin.routers import router as admin_router
from store.routers import router as store_router
from robot.routers import router as robot_router

app = FastAPI()

app.include_router(admin_router, prefix="/admin")
app.include_router(store_router, prefix="/store")
app.include_router(robot_router, prefix="/robot")

add_pagination(app)
