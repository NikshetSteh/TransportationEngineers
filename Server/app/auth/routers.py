from fastapi import APIRouter

from auth.client_type import ClientType
from auth.schemes import *
from auth.service import (create_login_code_for_client,
                          create_new_login_for_robot,
                          create_new_login_for_store, create_session)
from db import DbDependency, RedisDependency
from robot.schemes import Robot
from store_api.schemes import Store

router = APIRouter()


@router.post("/robot/new_login")
async def new_login(
        data: NewRobotLogin,
        db: DbDependency
) -> Robot:
    return await create_new_login_for_robot(
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
    token, request_id = await create_login_code_for_client(
        login_request.id,
        redis_pool,
        db,
        ClientType.ROBOT
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
        redis_pool,
        ClientType.ROBOT
    )

    return AuthResponse(token=session_id)


@router.post("/store/new_login")
async def new_login(
        data: NewStoreLogin,
        db: DbDependency
) -> Store:
    print("Store login code for", data.store_id)
    return await create_new_login_for_store(
        data.login,
        data.password,
        data.public_key,
        data.store_id,
        db
    )


@router.post("/store/login")
async def login(
        login_request: LoginRequest,
        redis_pool: RedisDependency,
        db: DbDependency
) -> LoginCode:
    print("Store login for", login_request.id)
    token, request_id = await create_login_code_for_client(
        login_request.id,
        redis_pool,
        db,
        ClientType.STORE
    )

    return LoginCode(
        data=token,
        request_id=request_id
    )


@router.post("/store/login_code")
async def login_code(
        login_data: LoginCode,
        redis_pool: RedisDependency,
) -> AuthResponse:
    print("Store login code for", login_data.request_id)
    session_id = await create_session(
        login_data.request_id,
        login_data.data,
        redis_pool,
        ClientType.STORE
    )

    return AuthResponse(token=session_id)
