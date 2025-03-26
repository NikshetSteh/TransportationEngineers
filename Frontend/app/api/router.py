from fastapi import APIRouter

from api.schemes import Profile
from login.service import AuthRequired


router = APIRouter(
    prefix="/api/v1",
)


@router.get("/users")
async def get_profile(
        user_data: AuthRequired
) -> Profile:
    return Profile(
        username=user_data["name"],
    )
