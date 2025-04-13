import os
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

import bcrypt
from fastapi import HTTPException, status
from jwt import encode


def create_access_token(data: dict[str, str]):
    to_encode = data.copy()
    expire = datetime.now(tz=ZoneInfo("UTC")) + timedelta(
        minutes=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
    )
    to_encode.update({"exp": expire})
    encoded_jwt = encode(to_encode, os.getenv("SECRET_KEY"),
                         algorithm=os.getenv("ALGORITHM"))

    return encoded_jwt


def get_password_hash(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed_password.decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode("utf-8"),
                          hashed_password.encode("utf-8"))


def validate_user_authorization(current_user_id: int, req_user_id: int):
    if current_user_id != req_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient rights"
        )
