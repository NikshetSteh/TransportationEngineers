from typing import Annotated

from fastapi import Depends

from auth.client_type import ClientType
from auth.service import auth_request

RobotAuthRequired = Annotated[str, Depends(auth_request(ClientType.ROBOT))]
StoreAuthRequired = Annotated[str, Depends(auth_request(ClientType.STORE))]
