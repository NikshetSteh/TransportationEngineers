from typing import Annotated

from fastapi import Depends

from app.auth.service import auth_request

AuthRequired = Annotated[str, Depends(auth_request)]
