import base64
import uuid

import cv2
import numpy as np
from fastapi import APIRouter, HTTPException
from fastapi_pagination import Page, paginate

from admin.schemes import *
from config import get_config
from db import ChromaDependency
from face_model import FaceModelDependency
from users.schemes import User

router = APIRouter()


@router.post("/add_user")
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
    if user["distances"][0][0] < config.THRESHOLD:
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
