from typing import Annotated

from fastapi import APIRouter, Depends, status

from recsys.features.auth.model import Auth, Token
from recsys.features.users.model import User
from recsys.features.auth.application import create_access_token, get_current_user

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)


@router.post("/token", status_code=status.HTTP_200_OK)
async def get_access_token(auth_req: Auth) -> Token:
    access_token = await create_access_token(auth_req)
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/refresh-token", status_code=status.HTTP_200_OK)
async def refresh_access_token(
    current_user: Annotated[User, Depends(get_current_user)]
) -> Token:
    new_access_token = await create_access_token(current_user.email)
    return {"access_token": new_access_token, "token_type": "bearer"}
