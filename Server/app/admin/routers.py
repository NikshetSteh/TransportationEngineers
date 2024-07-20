import base64
import uuid

import bcrypt
import cv2
import numpy as np
from fastapi import APIRouter, HTTPException
from fastapi_pagination import Page, paginate
from sqlalchemy import delete, select

from admin.schemes import *
from auth.engineer_privileges import engineer_privileges_translations
from config import get_config
from db import ChromaDependency, DbDependency
from face_model import FaceModelDependency
from model.engineer import Engineer as EngineerModel
from schemes import EmptyResponse
from users.schemes import User

router = APIRouter()


@router.post("/user")
async def add_user(
        data: UserCreation,
        chroma: ChromaDependency,
        model: FaceModelDependency
) -> User:
    image_bytes = base64.b64decode(data.face)
    image_array = np.frombuffer(image_bytes, dtype=np.uint8)
    image = cv2.imdecode(image_array, flags=cv2.IMREAD_COLOR)

    if image.shape[0] * image.shape[1] > 1000000:
        raise HTTPException(status_code=400, detail="Image too big")

    if image.shape[0] < 100 or image.shape[1] < 100:
        raise HTTPException(status_code=400, detail="Image too small")

    faces = model.get(image)

    if len(faces) > 1:
        raise HTTPException(status_code=400, detail="Too many faces")

    if len(faces) == 0:
        raise HTTPException(status_code=400, detail="No faces")

    face = faces[0]

    x1, y1, x2, y2 = face["bbox"]
    square = (x2 - x1) * (y2 - y1)

    if square / image.shape[0] / image.shape[1] < 0.4:
        raise HTTPException(status_code=400, detail="Face too small")

    embedding = face["embedding"]

    collection = await chroma.get_or_create_collection("faces")

    user = await collection.query(
        query_embeddings=embedding.tolist(),
        n_results=1
    )

    config = get_config()
    if len(user["distances"][0]) > 0 and user["distances"][0][0] < config.THRESHOLD:
        raise HTTPException(status_code=400, detail="User already exists")

    user_id = str(uuid.uuid4())

    await collection.add(
        ids=[user_id],
        embeddings=[embedding.tolist()],
        metadatas=[{"name": data.name}],
    )

    return User(id=user_id, name=data.name)


@router.get("/users")
async def get_users(
        chroma: ChromaDependency,
) -> Page[User]:
    collection = await chroma.get_or_create_collection("faces")
    data = await collection.peek(limit=await collection.count())
    users = []
    for i in range(len(data["ids"])):
        users.append(User(id=data["ids"][i], name=data["metadatas"][i]["name"]))

    return paginate(users)


@router.delete("/users/{user_id}")
async def delete_user(
        user_id: str,
        chroma: ChromaDependency
) -> EmptyResponse:
    collection = await chroma.get_or_create_collection("faces")
    await collection.delete(ids=[user_id])

    return EmptyResponse()


@router.post("/engineer")
async def create_engineer(
        data: EngineerCreation,
        db: DbDependency
) -> Engineer:
    async with db() as session:
        hashed_password = bcrypt.hashpw(
            data.password.encode("utf-8"),
            bcrypt.gensalt(12)
        ).decode("utf-8")

        engineer = EngineerModel(
            login=data.login,
            password=hashed_password
        )
        session.add(engineer)
        await session.commit()

    return Engineer(
        id=str(engineer.id),
        login=engineer.login
    )


@router.delete("/engineers/{engineer_id}")
async def delete_engineer(
        engineer_id: str,
        db: DbDependency
) -> EmptyResponse:
    async with db() as session:
        print(engineer_id)
        engineers = (await session.execute(
            select(EngineerModel).where(EngineerModel.id == engineer_id)
        )).one_or_none()

        if engineers is None:
            raise HTTPException(status_code=404, detail="Engineer not found")

        await session.execute(
            delete(EngineerModel).where(EngineerModel.id == engineer_id)
        )
        await session.commit()

    return EmptyResponse()


@router.get("/engineers")
async def get_engineer(
        db: DbDependency
) -> Page[Engineer]:
    async with db() as session:
        engineers = (await session.execute(
            select(EngineerModel)
        )).fetchall()

    data = list(
        map(
            lambda x: Engineer(
                id=str(x[0].id),
                login=x[0].login
            ),
            engineers
        )
    )
    return paginate(data)


@router.put("/engineer_privileges")
async def update_engineer(
        data: EngineerPrivilegesUpdate,
        db: DbDependency
) -> EmptyResponse:
    async with db() as session:
        engineers = (await session.execute(
            select(EngineerModel).where(EngineerModel.id == data.id)
        )).one_or_none()

        if engineers is None:
            raise HTTPException(status_code=404, detail="Engineer not found")

        engineer = engineers[0]

        privileges = 0
        for i in data.privileges:
            privileges |= engineer_privileges_translations[i]

        engineer.privileges = privileges
        session.add(engineer)
        await session.commit()

    return EmptyResponse()
