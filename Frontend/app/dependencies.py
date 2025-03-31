from typing import Annotated

from fastapi import Depends

from config import get_config

config = get_config()


def get_global_context():
    return {"ROBOT_API_URI": config.ROBOT_API_URI}


TEMPLATES_GLOBAL_CONTEXT = Annotated[dict, Depends(get_global_context)]
