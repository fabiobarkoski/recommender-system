from fastapi import status

from recsys.features.movies.model import MoviePublic, RatingPublic


def test_get_movies(client, mocker):
    mocker.patch("recsys.features.movies.application.get_movies",
                 return_value=[
                     MoviePublic(id=1, title="Awesome movie",
                                 genres=["Action"], actors=["DiCaprio"],
                                 directors=["Martin Scorsese"])
                 ])
    response = client.get("/movies")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [{
        "id": 1,
        "title": "Awesome movie",
        "genres": ["Action"],
        "actors": ["DiCaprio"],
        "directors": ["Martin Scorsese"]
    }]


def test_get_movie(client, mocker):
    mocker.patch("recsys.features.movies.application.get_movie",
                 return_value=MoviePublic(id=1, title="Awesome movie",
                                          genres=["Action"], actors=["DiCaprio"],
                                          directors=["Martin Scorsese"])
                 )
    response = client.get("/movies/1")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "id": 1,
        "title": "Awesome movie",
        "genres": ["Action"],
        "actors": ["DiCaprio"],
        "directors": ["Martin Scorsese"]
    }


def test_post_movie(client, mocker):
    mocker.patch("recsys.features.movies.application.create_movie",
                 return_value=MoviePublic(id=1, title="Awesome movie",
                                          genres=["Action"], actors=["DiCaprio"],
                                          directors=["Martin Scorsese"]))
    response = client.post(
        "/movies",
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


def test_patch_movie(client, mocker):
    mocker.patch("recsys.features.movies.application.update_movie",
                 return_value=MoviePublic(id=1, title="Foobar the movie",
                                          genres=["Action"], actors=["DiCaprio"],
                                          directors=["Martin Scorsese"]))
    response = client.patch(
        "/movies/1",
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


def test_get_movie_ratings(client, mocker):
    mocker.patch("recsys.features.movies.application.get_ratings",
                 return_value=[
                     RatingPublic(id=1, user_id=1, movie_id=1, rating=4)
                 ])
    response = client.get("/movies/1/ratings")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [{
        "id": 1,
        "user_id": 1,
        "movie_id": 1,
        "rating": 4
    }]


def test_post_movie_ratings(client, mocker):
    mocker.patch("recsys.features.movies.application.create_rating",
                 return_value=RatingPublic(id=1, user_id=1, movie_id=1, rating=4)
             )
    response = client.post(
        "/movies/1/ratings",
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


def test_get_user_recommendations(client, mocker):
    mocker.patch("recsys.features.movies.routes.user_recommendation",
                 return_value=[{
                     "id": 1,
                     "title": "Awesome movie",
                     "genres": ["Action"],
                     "actors": ["DiCaprio"],
                     "directors": ["Martin Scorsese"]
                 }])
    response = client.get("/movies/1/recommendations")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [{
        "id": 1,
        "title": "Awesome movie",
        "genres": ["Action"],
        "actors": ["DiCaprio"],
        "directors": ["Martin Scorsese"]
    }]


def test_get_user_ratings(client, mocker):
    mocker.patch("recsys.features.movies.application.get_user_ratings",
                 return_value=[{
                     "title": "Awesome movie",
                     "rating": 4
                 }])
    response = client.get("/movies/1/ratings/user")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [{
        "title": "Awesome movie",
        "rating": 4
    }]
