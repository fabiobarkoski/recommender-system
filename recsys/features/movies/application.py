import ast

from fastapi import HTTPException, status

from recsys.features.movies import repository
from recsys.common.database import postgres_connect
from recsys.features.ratings.model import RatingBase, RatingPublic
from recsys.features.movies.model import (
    Movie,
    MovieBase,
    MoviePublic,
    MovieUpdate,
)


async def get_movie(movie_id: int) -> Movie:
    movie = await repository.get_movie(movie_id)
    if not movie:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Movie not found")

    return movie


async def get_movies():
    movies = await repository.get_movies()
    return movies


async def create_movie(movie: MovieBase) -> MoviePublic:
    created_movie = await repository.create_movie(movie)
    return created_movie


async def update_movie(movie_id: int, movie: MovieUpdate):
    movie_db = await get_movie(movie_id)
    updated_movie = await repository.update_movie(movie_db, movie)
    return updated_movie


async def get_movie_ratings(movie_id: int) -> list[RatingPublic]:
    movie = await get_movie(movie_id)
    ratings = await repository.get_movie_ratings(movie)
    return ratings


async def create_movie_rating(
    movie_id: int, user_id: int, rating: RatingBase
) -> RatingPublic:
    movie = await get_movie(movie_id)
    created_rating = await repository.create_movie_rating(movie, user_id, rating)
    return created_rating


def create_movie_dumb(title: str, genres: list[str], actors: list[str] | None, directors: list[str] | None):
    parsed_genres = ast.literal_eval(genres) if genres else None
    parsed_genres = [p.strip() for p in parsed_genres] if parsed_genres else None
    parsed_actors = ast.literal_eval(actors) if actors else None
    parsed_actors = [p.strip() for p in parsed_actors] if parsed_actors else None
    parsed_directors = ast.literal_eval(directors) if directors else None
    parsed_directors = [p.strip() for p in parsed_directors] if parsed_directors else None
    movie = Movie(title=title, genres=parsed_genres,
                  actors=parsed_actors, directors=parsed_directors)
    return movie


async def batch_movie(movies: list[dict[str, str]]):
    async with postgres_connect() as conn:
        for m in movies:
            movie = create_movie_dumb(**m)
            conn.add(movie)
        await conn.commit()


if __name__ == "__main__":
    create_movie()
