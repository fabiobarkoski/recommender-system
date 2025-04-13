from fastapi import status

from recsys.features.movies.model import MoviePublic
from recsys.features.ratings.model import RatingPublic


def test_get_movies(client, mocker, token):
    mocker.patch("recsys.features.movies.application.get_movies",
                 return_value=[
                     MoviePublic(id=1, title="Awesome movie",
                                 genres=["Action"], actors=["DiCaprio"],
                                 directors=["Martin Scorsese"])
                 ])
    response = client.get(
        "/movies",
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


def test_get_movie(client, mocker, token):
    mocker.patch("recsys.features.movies.application.get_movie",
                 return_value=MoviePublic(id=1,
                                          title="Awesome movie",
                                          genres=["Action"],
                                          actors=["DiCaprio"],
                                          directors=["Martin Scorsese"])
                 )
    response = client.get(
        "/movies/1",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "id": 1,
        "title": "Awesome movie",
        "genres": ["Action"],
        "actors": ["DiCaprio"],
        "directors": ["Martin Scorsese"]
    }


def test_post_movie(client, mocker, token):
    mocker.patch("recsys.features.movies.application.create_movie",
                 return_value=MoviePublic(id=1,
                                          title="Awesome movie",
                                          genres=["Action"],
                                          actors=["DiCaprio"],
                                          directors=["Martin Scorsese"]))
    response = client.post(
        "/movies",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "title": "Awesome movie",
            "genres": ["Action"],
            "actors": ["DiCaprio"],
            "directors": ["Martin Scorsese"]
        }
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == {
        "id": 1,
        "title": "Awesome movie",
        "genres": ["Action"],
        "actors": ["DiCaprio"],
        "directors": ["Martin Scorsese"]
    }


def test_patch_movie(client, mocker, token):
    mocker.patch("recsys.features.movies.application.update_movie",
                 return_value=MoviePublic(id=1,
                                          title="Foobar the movie",
                                          genres=["Action"],
                                          actors=["DiCaprio"],
                                          directors=["Martin Scorsese"]))
    response = client.patch(
        "/movies/1",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "title": "Foobar the movie"
        }
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "id": 1,
        "title": "Foobar the movie",
        "genres": ["Action"],
        "actors": ["DiCaprio"],
        "directors": ["Martin Scorsese"]
    }


def test_delete_movie(client, mocker, token):
    mocker.patch("recsys.features.movies.application.delete_movie")

    response = client.delete(
        "/movies/1",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"message": "Movie deleted"}


def test_get_movie_ratings(client, mocker, token):
    mocker.patch("recsys.features.movies.application.get_movie_ratings",
                 return_value=[
                     RatingPublic(id=1, user_id=1, movie_id=1, rating=4)
                 ])
    response = client.get(
        "/movies/1/ratings",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [{
        "id": 1,
        "user_id": 1,
        "movie_id": 1,
        "rating": 4
    }]


def test_post_movie_ratings(client, mocker, token):
    mocker.patch("recsys.features.movies.application.create_movie_rating",
                 return_value=RatingPublic(id=1, user_id=1,
                                           movie_id=1, rating=4))
    response = client.post(
        "/movies/1/ratings",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "user_id": 1,
            "rating": 4
        }
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == {
        "id": 1,
        "user_id": 1,
        "movie_id": 1,
        "rating": 4
    }
