import base64

import cv2
import numpy as np
from chromadb.api import AsyncClientAPI
from config import get_config
from fastapi import HTTPException
from insightface.app import FaceAnalysis


async def search_face(
    image: str, face_model: FaceAnalysis, chroma_db: AsyncClientAPI
) -> None | str:
    image_bytes = base64.b64decode(image)
    image_array = np.frombuffer(image_bytes, dtype=np.uint8)
    image = cv2.imdecode(image_array, flags=cv2.IMREAD_COLOR)

    faces = face_model.get(image)

    if len(faces) == 0:
        raise HTTPException(status_code=400, detail="No faces")

    faces_by_square = sorted(
        faces,
        key=lambda x: (x["bbox"][2] - x["bbox"][0]) * (x["bbox"][3] - x["bbox"][1]),
    )

    face = faces_by_square[0]

    x1, y1, x2, y2 = face["bbox"]
    square = (x2 - x1) * (y2 - y1)

    # if square / image.shape[0] / image.shape[1] < 0.05:
    #     raise HTTPException(status_code=400, detail="Too small square")

    collection = await chroma_db.get_or_create_collection("faces")
    users = await collection.query(
        query_embeddings=face["embedding"].tolist(), n_results=1
    )

    config = get_config()

    if len(users["distances"][0]) == 0:
        return None

    if users["distances"][0][0] > config.THRESHOLD:
        raise HTTPException(status_code=400, detail="Not found")

    user_id = users["ids"][0][0]

    return user_id


async def save_face(
    image: str, user_id: str, model: FaceAnalysis, chroma_db: AsyncClientAPI
) -> None:
    image_bytes = base64.b64decode(image)
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

    # if square / image.shape[0] / image.shape[1] < 0.4:
    #     raise HTTPException(status_code=400, detail="Face too small")

    embedding = face["embedding"]

    collection = await chroma_db.get_or_create_collection("faces")

    user = await collection.query(query_embeddings=embedding.tolist(), n_results=1)

    config = get_config()
    if len(user["distances"][0]) > 0 and user["distances"][0][0] < config.THRESHOLD:
        raise HTTPException(status_code=409, detail="User already exists")

    await collection.add(
        ids=[user_id],
        embeddings=[embedding.tolist()],
    )


async def delete_face(user_id: str, chroma_db: AsyncClientAPI) -> None:
    collection = await chroma_db.get_or_create_collection("faces")
    await collection.delete(ids=[user_id])


async def get_all_users(chroma_db: AsyncClientAPI) -> list[str]:
    collection = await chroma_db.get_or_create_collection("faces")
    users = await collection.query(n_results=await collection.count())
    return users["ids"]
