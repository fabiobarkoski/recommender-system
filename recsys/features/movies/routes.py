from typing import Annotated

from fastapi import APIRouter, Depends, status

from recsys.features.users.model import User
from recsys.features.movies import application
from recsys.features.auth.application import get_current_user
from recsys.features.ratings.model import RatingBase, RatingPublic
from recsys.features.movies.model import (
    MovieBase,
    MoviePublic,
    MovieUpdate,
)

router = APIRouter(
    prefix="/movies",
    tags=["movies"]
)


@router.get("/", status_code=status.HTTP_200_OK)
async def get_movies() -> list[MoviePublic]:
    movies = await application.get_movies()
    return movies


@router.get("/{movie_id}", status_code=status.HTTP_200_OK)
async def get_movie(movie_id: int) -> MoviePublic:
    movie = await application.get_movie(movie_id)
    return movie


@router.post("/", status_code=status.HTTP_201_CREATED)
async def post_movie(movie: MovieBase) -> MoviePublic:
    created_movie = await application.create_movie(movie)
    return created_movie


@router.patch("/{movie_id}", status_code=status.HTTP_200_OK)
async def patch_movie(movie_id: int, movie: MovieUpdate) -> MoviePublic:
    updated_movie = await application.update_movie(movie_id, movie)
    return updated_movie


@router.get("/{movie_id}/ratings", status_code=status.HTTP_200_OK)
async def get_movie_ratings(movie_id: int) -> list[RatingPublic]:
    ratings = await application.get_movie_ratings(movie_id)
    return ratings


@router.post("/{movie_id}/ratings", status_code=status.HTTP_201_CREATED)
async def post_movie_rating(
    movie_id: int, rating: RatingBase,
    current_user: Annotated[User, Depends(get_current_user)]
) -> RatingPublic:
    created_rating = await application.create_movie_rating(
                                                     movie_id,
                                                     current_user.id, rating
                                                 )
    return created_rating
