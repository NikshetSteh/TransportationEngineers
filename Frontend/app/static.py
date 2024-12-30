from starlette.staticfiles import StaticFiles
from starlette.routing import Router


static_router = Router()

static_router.mount("/", StaticFiles(directory="static"), name="static")
