from admin.routers import router as admin_router
from auth.routers import router as auth_router
from db import create_db_connection_factory
from fastapi import APIRouter, FastAPI
from fastapi_pagination import add_pagination
from frontend.routers import router as frontend_router
from keycloak.router import router as keycloak_user_router
from robot.routers import router as robot_router


async def lifespan(_):
    await create_db_connection_factory()
    yield


# noinspection PyTypeChecker
app = FastAPI(lifespan=lifespan)

api = APIRouter()

api.include_router(admin_router, prefix="/admin")
api.include_router(robot_router, prefix="/robot")
api.include_router(auth_router, prefix="/auth")
api.include_router(frontend_router, prefix="/frontend")
api.include_router(keycloak_user_router, prefix="/user-provider")

app.include_router(api, prefix="/base_api/v1")

add_pagination(app)
