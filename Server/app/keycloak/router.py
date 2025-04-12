from fastapi import APIRouter

from db import DbDependency
from keycloak.schemes import *
from keycloak.service import *
from users.service import delete_user

router = APIRouter()


@router.post("/users")
async def create_user_handler(
    user: ProvidedUserCreation, db: DbDependency
) -> ProvidedUser:
    return await create_user(user, db)


@router.patch("/users/{user_id}")
async def update_user_handler(
    user_id: str, user: ProvidedUserPatch, db: DbDependency
) -> ProvidedUser:
    return await update_user(user_id, user, db)


@router.delete("/users/{user_id}", status_code=204)
async def delete_user_handler(user_id: str, db: DbDependency) -> None:
    return await delete_user(user_id, db)


@router.get("/users/id/{user_id}")
async def get_user_by_id_handler(user_id: str, db: DbDependency) -> ProvidedUser:
    user =  await get_user_by_attribute("id", user_id, db)

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return user


@router.get("/users/username/{username}")
async def get_user_by_username_handler(username: str, db: DbDependency) -> ProvidedUser:
    user = await get_user_by_attribute("username", username, db)
    if user is None:
        user = await get_user_by_attribute("email", username, db)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.get("/users/email/{email}")
async def get_user_by_email_handler(email: str, db: DbDependency) -> ProvidedUser:
    return await get_user_by_attribute("email", email, db)


@router.get("/users/validate")
async def validate_user_credentials_handler(
    user_credentials: UserCredentials, db: DbDependency
) -> CredentialsValidationResult:
    return CredentialsValidationResult(
        valid=await validate_user_credential(
            user_credentials.user_id, user_credentials.password, db
        )
    )


@router.get("/users/all")
async def get_all_users_handler(
    # query: UserQuery,
    db: DbDependency,
) -> list[ProvidedUser]:
    # print(query)
    # print(query.model_dump_json(indent=4))
    # raise Exception("Not implemented")
    return await get_all_users(db)
