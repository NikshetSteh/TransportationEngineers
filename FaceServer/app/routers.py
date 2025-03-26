from fastapi import APIRouter, HTTPException

from db import ChromaDependency
from face_model import FaceModelDependency
from schemes import *
from service import delete_face, save_face, search_face

router = APIRouter()


@router.post("/face")
async def add_face_handler(
        request: NewFaceRequest,
        face_model: FaceModelDependency,
        chromadb: ChromaDependency
) -> EmptyResponse:
    await save_face(request.image, request.user_id, face_model, chromadb)
    return EmptyResponse()


@router.post("/search")
async def search_face_handler(
        request: SearchFaceRequest,
        face_model: FaceModelDependency,
        chromadb: ChromaDependency
) -> User:
    user_id = await search_face(request.image, face_model, chromadb)
    if user_id is None:
        raise HTTPException(status_code=404, detail="User not found")

    return User(user_id=user_id)


@router.delete("/face/{user_id}")
async def delete_face_handler(
        user_id: str,
        chromadb: ChromaDependency
) -> EmptyResponse:
    await delete_face(user_id, chromadb)
    return EmptyResponse()


@router.get("/faces")
async def get_faces_handler(
    chromadb: ChromaDependency
) -> list[User]:
    collection = await chromadb.get_or_create_collection("faces")
    users = await collection.get()
    return [User(user_id=user_id) for user_id in users["ids"]]
