import aiohttp
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from config import get_config
import urllib.parse as urllib

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
    if code is None:
        if "refresh_token" in request.cookies:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                        config.auth_token_uri,
                        data={
                            "client_id": config.client_id,
                            "client_secret": config.client_secret,
                            "grant_type": "refresh_token",
                            "refresh_token": request.cookies["refresh_token"],
                        },
                ) as response:
                    if response.status == 200:
                        data = await response.json()

                        response = RedirectResponse(
                            url="http://localhost:8000/"
                        )

                        response.set_cookie("access_token", data["access_token"])
                        response.set_cookie("refresh_token", data["refresh_token"])

                        return response

        return RedirectResponse(
            url=config.auth_redirect_uri + "?" + urllib.urlencode({
                "response_type": "code",
                "client_id": config.client_id,
                "redirect_uri": request.url_for("auth"),
            })
        )

    async with aiohttp.ClientSession() as session:
        async with session.post(
                config.auth_token_uri,
                data={
                    "client_id": config.client_id,
                    "client_secret": config.client_secret,
                    "grant_type": "authorization_code",
                    "code": code,
                    "redirect_uri": request.url_for("auth"),
                },
        ) as response:
            data = await response.json()

            response = RedirectResponse(
                url=request.url_for("root")
            )

            response.set_cookie("access_token", data["access_token"], expires=data["expires_in"])
            response.set_cookie("refresh_token", data["refresh_token"], expires=data["refresh_expires_in"])

            return response
