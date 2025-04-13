from fastapi import status

from recsys.features.users.model import UserPublic


def test_get_users(client, mocker, token):
    mocker.patch("recsys.features.users.application.get_users",
                 return_value=[UserPublic(id=1, name="test",
                                          email="test@test.com")])
    response = client.get(
        "/users",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [{
        "id": 1,
        "name": "test",
        "email": "test@test.com"
    }]


def test_get_user(client, mocker, token):
    mocker.patch("recsys.features.users.application.get_user",
                 return_value=UserPublic(id=1, name="test",
                                         email="test@test.com"))
    response = client.get(
        "/users/1",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "id": 1,
        "name": "test",
        "email": "test@test.com"
    }


def test_post_user(client, mocker):
    mocker.patch("recsys.features.users.application.create_user",
                 return_value=UserPublic(id=1, name="test",
                                         email="test@test.com"))
    response = client.post(
        "/users",
        json={
            "name": "test",
            "email": "test@test.com",
            "password": "abc123"
        }
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == {
        "id": 1,
        "name": "test",
        "email": "test@test.com"
    }


def test_patch_user(client, mocker, token):
    mocker.patch("recsys.features.users.application.update_user",
                 return_value=UserPublic(id=1, name="foobar",
                                         email="test@test.com"))
    response = client.patch(
        "/users/1",
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "name": "foobar"
        }
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "id": 1,
        "name": "foobar",
        "email": "test@test.com"
    }


def test_delete_user(client, mocker, token):
    mocker.patch("recsys.features.users.application.delete_user")

    response = client.delete(
        "/users/1",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"message": "User deleted"}


def test_user_recommendations(client, mocker, token):
    mocker.patch("recsys.features.users.application.user_recommendation",
                 return_value=[{
                     "id": 1,
                     "title": "Awesome movie",
                     "genres": ["Action"],
                     "actors": ["DiCaprio"],
                     "directors": ["Martin Scorsese"]
                 }])
    response = client.get(
        "users/recommendations",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [{
        "id": 1,
        "title": "Awesome movie",
        "genres": ["Action"],
        "actors": ["DiCaprio"],
        "directors": ["Martin Scorsese"]
    }]


def test_user_ratings(client, mocker, token):
    mocker.patch("recsys.features.users.application.get_ratings",
                 return_value=[{
                     "title": "Awesome movie",
                     "rating": 4
                 }])
    response = client.get(
        "/users/ratings",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [{
        "title": "Awesome movie",
        "rating": 4
    }]
