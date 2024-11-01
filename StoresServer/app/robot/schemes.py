import re
from typing import Annotated

from pydantic import AfterValidator, BaseModel, Field


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
