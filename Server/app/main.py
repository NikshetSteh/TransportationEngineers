from fastapi import FastAPI
from fastapi_pagination import add_pagination

from admin.routers import router as admin_router
from auth.routers import router as auth_router
from db import create_db_connection_factory
from robot.routers import router as robot_router


async def lifespan(_):
    await create_db_connection_factory()
    yield


# noinspection PyTypeChecker
app = FastAPI(lifespan=lifespan)

app.include_router(admin_router, prefix="/admin")
app.include_router(robot_router, prefix="/robot")
app.include_router(auth_router, prefix="/auth")

add_pagination(app)
