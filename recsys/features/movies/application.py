
from fastapi import HTTPException, status

from recsys.features.movies import repository
from recsys.features.movies.model import (
    Movie,
    MovieBase,
    MoviePublic,
    MovieUpdate,
)
from recsys.features.ratings.model import RatingBase, RatingPublic


async def get_movie(movie_id: int) -> Movie:
    movie = await repository.get_movie(movie_id)
    if not movie:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Movie not found"
        )

    return movie


async def get_movies(skip: int, limit: int):
    movies = await repository.get_movies(skip, limit)
    return movies


async def create_movie(movie: MovieBase) -> MoviePublic:
    created_movie = await repository.create_movie(movie)
    return created_movie


async def update_movie(movie_id: int, movie: MovieUpdate):
    movie_db = await get_movie(movie_id)
    updated_movie = await repository.update_movie(movie_db, movie)
    return updated_movie


async def delete_movie(movie_id: int):
    await repository.delete_movie(movie_id)


async def get_movie_ratings(movie_id: int) -> list[RatingPublic]:
    ratings = await repository.get_movie_ratings(movie_id)
    return ratings


async def create_movie_rating(
    movie_id: int, user_id: int, rating: RatingBase
) -> RatingPublic:
    if not (0 <= rating.rating <= 5):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Rating must be between 0 and 5"
        )
    movie = await get_movie(movie_id)
    created_rating = await repository.create_movie_rating(movie, user_id,
                                                          rating)
    return created_rating
