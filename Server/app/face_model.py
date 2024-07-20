from typing import Annotated

from fastapi import Depends
from insightface.app import FaceAnalysis

from config import get_config

model = None


def get_model() -> FaceAnalysis:
    global model

    if model is not None:
        return model

    config = get_config()

    model = FaceAnalysis(name=config.FACE_MODEL, provider=[config.FACE_MODEL_PROVIDER])
    model.prepare(ctx_id=0, det_size=(config.FACE_MODEL_DET_SIZE, config.FACE_MODEL_DET_SIZE))

    return model


FaceModelDependency = Annotated[FaceAnalysis, Depends(get_model)]
