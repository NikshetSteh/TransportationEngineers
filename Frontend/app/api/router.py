import base64
import io

from fastapi import APIRouter, File, UploadFile, HTTPException
from aiohttp.client import ClientSession

from api.schemes import Profile, EmptyResponse
from login.service import AuthRequired
from config import get_config
from PIL import Image

router = APIRouter(
    prefix="/api/v1",
)

config = get_config()


@router.get("/users")
async def get_profile(
        user_data: AuthRequired
) -> Profile:
    return Profile(
        username=user_data["name"],
    )


@router.post("/users/face")
async def add_biometric(
        user_data: AuthRequired,
        file: UploadFile = File(...)
) -> EmptyResponse:
    contents = await file.read()
    if len(contents) > config.MAX_IMAGE_SIZE:
        raise HTTPException(status_code=400, detail="File is too large (max 1.25MB).")

    image = Image.open(io.BytesIO(contents))

    if image.format not in ["PNG", "JPEG", "JPG"]:
        raise HTTPException(status_code=400, detail=f"Unsupported image format. Allowed: PNG, JPEG, JPG")

    if image.width < 100 or image.height < 100:
        raise HTTPException(status_code=400, detail=f"Image too small. Min size: {100}x{100}px")

    if image.width > 10_000 or image.height > 10_000:
        raise HTTPException(status_code=400, detail=f"Image too large")

    buffered = io.BytesIO()
    image.save(buffered, format="JPEG")
    image_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")

    async with ClientSession() as session:
        async with session.post(
                config.API_URI + "/base_api/v1/frontend/face",
                headers={
                    "Authorization": f"Bearer {user_data['access_token']}"
                },
                json={
                    "face": image_base64,
                }
        ) as response:
            if response.status != 200:
                raise HTTPException(status_code=response.status, detail=await response.text())

    return EmptyResponse()
