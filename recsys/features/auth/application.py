import os
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt import DecodeError, ExpiredSignatureError, decode

from recsys.common import security
from recsys.features.auth.model import Auth
from recsys.features.users.model import User
from recsys.features.users.repository import get_user_by_email

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)]
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )

    try:
        payload = decode(token, os.getenv("SECRET_KEY"),
                         algorithms=os.getenv("ALGORITHM"))
        subject = payload.get("sub")

        if not subject:
            raise credentials_exception
    except (ExpiredSignatureError, DecodeError):
        raise credentials_exception

    user = await get_user_by_email(subject)

    if not user:
        raise credentials_exception

    return user


async def create_access_token(auth_req: Auth) -> str:
    user = await get_user_by_email(auth_req.email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )

    if not security.verify_password(auth_req.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )

    access_token = security.create_access_token(data={"sub": user.email})

    return access_token
