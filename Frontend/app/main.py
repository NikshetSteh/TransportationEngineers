from fastapi import FastAPI
from static import static_router

from router import router

app = FastAPI()

app.include_router(router)

app.mount("/static", static_router, name="static")
