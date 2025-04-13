from fastapi import status

from recsys.features.ratings.model import Rating, RatingPublic


def test_get_ratings(client, mocker, token):
    mocker.patch("recsys.features.ratings.application.get_ratings",
                 return_value=[RatingPublic(id=1, user_id=1,
                                            movie_id=1, rating=5)])
    response = client.get(
        "/ratings",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [{
        "id": 1,
        "user_id": 1,
        "movie_id": 1,
        "rating": 5
    }]


def test_update_rating(client, mocker, token):
    mocker.patch("recsys.features.ratings.application.get_rating",
                 return_value=Rating(id=1, user_id=1,
                                     movie_id=1, rating=5))
    mocker.patch("recsys.features.ratings.application.update_rating",
                 return_value=RatingPublic(id=1, user_id=1,
                                           movie_id=1, rating=3))
    response = client.patch(
        "/ratings/1",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "rating": 3,
        }
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "id": 1,
        "user_id": 1,
        "movie_id": 1,
        "rating": 3
    }


def test_delete_rating(client, mocker, token):
    mocker.patch("recsys.features.ratings.application.get_rating",
                 return_value=Rating(id=1, user_id=1,
                                     movie_id=1, rating=5))
    mocker.patch("recsys.features.ratings.application.delete_rating")

    response = client.delete(
        "/ratings/1",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"message": "Rating deleted"}
