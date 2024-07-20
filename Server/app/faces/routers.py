import base64

import numpy as np
from fastapi import APIRouter, HTTPException

from config import get_config
from db import ChromaDependency
from faces.schemes import *
from face_model import FaceModelDependency

import cv2

router = APIRouter()


@router.post("/identification")
async def identification(
        request: IdentificationRequest,
        model: FaceModelDependency,
        chroma: ChromaDependency
) -> IdentificationResponse:
    image_bytes = base64.b64decode(request.image)
    image_array = np.frombuffer(image_bytes, dtype=np.uint8)
    image = cv2.imdecode(image_array, flags=cv2.IMREAD_COLOR)

    faces = model.get(image)

    if len(faces) == 0:
        raise HTTPException(status_code=400, detail="No faces")

    faces_by_square = sorted(faces, key=lambda x: (x["bbox"][2] - x["bbox"][0]) * (x["bbox"][3] - x["bbox"][1]))

    face = faces_by_square[0]

    x1, y1, x2, y2 = face["bbox"]
    square = (x2 - x1) * (y2 - y1)

    if square / image.shape[0] / image.shape[1] < 0.4:
        raise HTTPException(status_code=400, detail="Too small square")

    collection = await chroma.get_or_create_collection("faces")
    users = await collection.query(
        query_embeddings=face["embedding"].tolist(),
        n_results=1
    )

    config = get_config()

    if users["distances"][0][0] > config.THRESHOLD:
        raise HTTPException(status_code=400, detail="Not found")

    return IdentificationResponse(user_id=users["ids"][0][0], user_name=users["metadatas"][0][0]["name"])

