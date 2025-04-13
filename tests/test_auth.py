from fastapi import status

from recsys.common.security import get_password_hash
from recsys.features.users.model import User


def test_login_token(client, mocker):
    mocker.patch("recsys.features.auth.application.get_user_by_email",
                 return_value=User(
                                   id=1, name="test",
                                   email="test@test.com",
                                   password=get_password_hash("abc123")
                               ))
    response = client.post(
        "/auth/token",
        json={
            "email": "test@test.com",
            "password": "abc123",
        }
    )

    token = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert "access_token" in token
    assert "token_type" in token
    assert token["token_type"] == "bearer"


def test_refresh_token(client, token):
    response = client.post(
        "/auth/refresh-token",
        headers={"Authorization": f"Bearer {token}"},
    )

    token = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert "access_token" in token
    assert "token_type" in token
    assert token["token_type"] == "bearer"
