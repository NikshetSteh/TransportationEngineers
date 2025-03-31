from typing import Annotated

from auth.client_type import ClientType
from auth.service import auth_request
from fastapi import Depends

RobotAuthRequired = Annotated[str, Depends(auth_request(ClientType.ROBOT))]
StoreAuthRequired = Annotated[str, Depends(auth_request(ClientType.STORE))]
