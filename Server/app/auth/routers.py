from fastapi import APIRouter

from auth.schemes import *
from auth.service import create_new_login, create_session, generate_login_code
from db import DbDependency, RedisDependency
from robot.schemes import Robot

router = APIRouter()


@router.post("/robot/new_login")
async def new_login(
        data: NewLogin,
        db: DbDependency
) -> Robot:
    return await create_new_login(
        data.login,
        data.password,
        data.public_key,
        data.robot_model_id,
        data.robot_model_name,
        db
    )


@router.post("/robot/login")
async def login(
        login_request: LoginRequest,
        redis_pool: RedisDependency,
        db: DbDependency
) -> LoginCode:
    token, request_id = await generate_login_code(
        login_request.id,
        redis_pool,
        db
    )

    return LoginCode(
        data=token,
        request_id=request_id
    )


@router.post("/robot/login_code")
async def login_code(
        login_data: LoginCode,
        redis_pool: RedisDependency,
) -> AuthResponse:
    session_id = await create_session(
        login_data.request_id,
        login_data.data,
        redis_pool
    )

    return AuthResponse(token=session_id)
