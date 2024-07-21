from fastapi import APIRouter, HTTPException

from db import DbDependency
from robot.schemes import *
from robot.service import identification_face
from users.schemes import User

router = APIRouter()


@router.post("/identification")
async def identification(
        request: IdentificationRequest,
        db: DbDependency
) -> User:
    user = await identification_face(request.image, db)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return user
