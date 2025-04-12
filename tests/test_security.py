import os

from jwt import decode
from fastapi import status

from recsys.common.security import create_access_token


def test_jwt():
    data = {"test": "test"}

    token = create_access_token(data)

    decoded = decode(token, os.getenv("SECRET_KEY"), algorithms="HS256")

    assert decoded["test"] == data["test"]
    assert "exp" in decoded


def test_invalid_jwt_token(client, mocker):
    response = client.patch(
        "/users/1",
        headers={
            "Authorization": "Bearer invalid"
        },
        json={
            "name": "foobar"
        }
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {"detail": "Could not validate credentials"}
