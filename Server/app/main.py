from fastapi import FastAPI
from fastapi_pagination import add_pagination
from admin.routers import router as admin_router
from faces.routers import router as faces_roter

app = FastAPI()

app.include_router(admin_router, prefix="/admin")
app.include_router(faces_roter, prefix="/faces")

add_pagination(app)
