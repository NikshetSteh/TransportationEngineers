from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()

templates = Jinja2Templates(directory="templates")


@router.get("/")
async def root(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(
        request=request, name="index.html"
    )


@router.get("/login")
async def login(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(
        request=request, name="login.html"
    )


@router.get("/face_login")
async def face_login(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(
        request=request, name="face_login.html"
    )


@router.get("/qr_login")
async def qr_login(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(
        request=request, name="qr_login.html"
    )
