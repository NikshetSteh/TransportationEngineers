import base64
import urllib.parse as urllib

from fastapi import APIRouter, Request
from starlette.responses import RedirectResponse

from config import get_config
from login.schemes import RefreshTokenResponse
from login.service import get_token, get_user_data

router = APIRouter()

config = get_config()


@router.get("/login")
async def auth(request: Request, code: str = None) -> RedirectResponse:
    if code is None and "refresh_token" not in request.cookies:
        return RedirectResponse(
            url=config.AUTH_REDIRECT_URI + "?" + urllib.urlencode({
                "response_type": "code",
                "client_id": config.CLIENT_ID,
                "redirect_uri": request.url_for("auth") if config.FRONTEND_URL is None else f"{config.FRONTEND_URL}/login",
            })
        )

    if code is not None:
        access_token, expires_in, refresh_token, refresh_expires_in = await get_token(
            code,
            "authorization_code",
            str(request.url_for("auth") if config.FRONTEND_URL is None else f"{config.FRONTEND_URL}/login")
        )
    else:
        if "refresh_token" in request.cookies:
            try:
                access_token, expires_in, refresh_token, refresh_expires_in = await get_token(
                    request.cookies.get(
                        "refresh_token"
                    ),
                    "refresh_token",
                    str(request.url_for("auth") if config.FRONTEND_URL is None else f"{config.FRONTEND_URL}/login")
                )
            except Exception:
                return RedirectResponse(
                    url=config.AUTH_REDIRECT_URI + "?" + urllib.urlencode({
                        "response_type": "code",
                        "client_id": config.CLIENT_ID,
                        "redirect_uri": request.url_for("auth") if config.FRONTEND_URL is None else f"{config.FRONTEND_URL}/login",
                    })
                )
        else:
            return RedirectResponse(
                url=config.AUTH_REDIRECT_URI + "?" + urllib.urlencode({
                    "response_type": "code",
                    "client_id": config.CLIENT_ID,
                    "redirect_uri": request.url_for("auth") if config.FRONTEND_URL is None else f"{config.FRONTEND_URL}/login",
                })
            )

    user_data = await get_user_data(access_token)

    response = RedirectResponse(
        url=request.url_for("profile") if config.FRONTEND_URL is None else f"{config.FRONTEND_URL}/profile",
    )

    response.charset = "utf-8"

    response.set_cookie("access_token", access_token, expires=expires_in)
    response.set_cookie("refresh_token", refresh_token, expires=refresh_expires_in)
    response.set_cookie("given_name", base64.b64encode(user_data["given_name"].encode()).decode())
    response.set_cookie("user_id", user_data["sub"])

    return response


@router.post("/api/refresh")
async def refresh(request: Request):
    try:
        access_token, expires_in, refresh_token, refresh_expires_in = await get_token(
            request.cookies.get(
                "refresh_token"
            ),
            "refresh_token",
            str(request.url_for("auth") if config.FRONTEND_URL is None else f"{config.FRONTEND_URL}/login")
        )
    except Exception:
        return RedirectResponse(
            url=config.AUTH_REDIRECT_URI + "?" + urllib.urlencode({
                "response_type": "code",
                "client_id": config.CLIENT_ID,
                "redirect_uri": request.url_for("auth") if config.FRONTEND_URL is None else f"{config.FRONTEND_URL}/login",
            })
        )

    return RefreshTokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        expire_in=expires_in,
        refresh_expire_in=refresh_expires_in
    )

