from fastapi import FastAPI
from fastapi_pagination import add_pagination

from admin.routers import router as admin_router

app = FastAPI()

app.include_router(admin_router, prefix="/admin")

add_pagination(app)
