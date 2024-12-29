from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

router = APIRouter()

router.mount("/site", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


@router.get("/")
async def root(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(
        request=request, name="index.html"
    )
