from fastapi import FastAPI

from exceptions import UnauthorizedException
from login.service import auth_exception_handler
from static import static_router

from router import router as main_router
from login.router import router as login_router
from api.router import router as api_router

app = FastAPI()

app.include_router(main_router)
app.include_router(login_router)
app.include_router(api_router)

# noinspection PyTypeChecker
app.add_exception_handler(UnauthorizedException, auth_exception_handler)

app.mount("/site/static", static_router, name="static")
