import pytest
from fastapi.testclient import TestClient

from recsys.main import app
from recsys.features.users.model import User
from recsys.common.security import get_password_hash


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def token(client, mocker):
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
            "password": "abc123"
        }
    )

    return response.json()["access_token"]
