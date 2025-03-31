from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from config import get_config
from login.service import AuthRequired

from dependencies import TEMPLATES_GLOBAL_CONTEXT

config = get_config()

router = APIRouter()

templates = Jinja2Templates(directory="templates")


@router.get("/")
async def root(request: Request, template_context: TEMPLATES_GLOBAL_CONTEXT) -> HTMLResponse:
    return templates.TemplateResponse(
        request=request, name="index.html", context=template_context
    )


@router.get("/profile")
async def profile(
        request: Request,
        _: AuthRequired,
        template_context: TEMPLATES_GLOBAL_CONTEXT
) -> HTMLResponse:
    return templates.TemplateResponse(
        request=request, name="profile.html", context={"authed": "access_token" in request.cookies, **template_context}
    )


@router.get("/ticket")
async def ticket(
        request: Request,
        _: AuthRequired,
        template_context: TEMPLATES_GLOBAL_CONTEXT
) -> HTMLResponse:
    return templates.TemplateResponse(
        request=request, name="ticket.html", context={"authed": "access_token" in request.cookies, **template_context}
    )


@router.post("/ticket-ready")
async def ticket_ready(
        request: Request,
        _: AuthRequired,
        template_context: TEMPLATES_GLOBAL_CONTEXT
) -> HTMLResponse:
    return templates.TemplateResponse(
        request=request, name="ready-ticket.html", context={"authed": "access_token" in request.cookies, **template_context}
    )


@router.get("/bio")
async def bio(
        request: Request,
        _: AuthRequired,
        template_context: TEMPLATES_GLOBAL_CONTEXT
) -> HTMLResponse:
    return templates.TemplateResponse(
        request=request, name="bio.html", context={"authed": "access_token" in request.cookies, **template_context}
    )
