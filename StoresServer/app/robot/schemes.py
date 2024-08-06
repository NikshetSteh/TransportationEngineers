import re

from pydantic import BaseModel, Field, AfterValidator
from typing import Annotated


def check_id(data: list[str]) -> list[str]:
    for i in data:
        assert re.fullmatch("^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$", i)

    return data


IdList = Annotated[list[str], AfterValidator(check_id)]


class StoreListRequest(BaseModel):
    ids: IdList = Field(
        min_length=1,
        max_length=50,
    )
