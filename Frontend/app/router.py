import urllib.parse as urllib

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from config import get_config
from service import get_token, get_user_data

config = get_config()

router = APIRouter()

templates = Jinja2Templates(directory="templates")


@router.get("/")
async def root(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(
        request=request, name="index.html"
    )


@router.get("/login")
async def auth(request: Request, code: str = None) -> RedirectResponse:
    if code is None and "refresh_token" not in request.cookies:
        return RedirectResponse(
            url=config.auth_redirect_uri + "?" + urllib.urlencode({
                "response_type": "code",
                "client_id": config.client_id,
                "redirect_uri": request.url_for("auth"),
            })
        )

    if "refresh_token" in request.cookies:
        access_token, expires_in, refresh_token, refresh_expires_in = await get_token(
            request.cookies.get(
                "refresh_token"
            ),
            "refresh_token",
            str(request.url_for("auth"))
        )
    else:
        access_token, expires_in, refresh_token, refresh_expires_in = await get_token(
            code,
            "authorization_code",
            str(request.url_for("auth"))
        )

    user_data = await get_user_data(access_token)

    response = RedirectResponse(
        url=request.url_for("profile")
    )

    response.set_cookie("access_token", access_token, expires=expires_in)
    response.set_cookie("refresh_token", refresh_token, expires=refresh_expires_in)
    response.set_cookie("given_name", user_data["given_name"])
    response.set_cookie("user_id", user_data["sub"])

    return response


@router.get("/profile")
async def profile(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(
        request=request, name="profile.html", context={"authed": "access_token" in request.cookies}
    )
