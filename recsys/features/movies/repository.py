from sqlalchemy.orm import selectinload
from sqlmodel import select

from recsys.common.database import postgres_connect
from recsys.features.movies.model import (
    Movie,
    MovieBase,
    MovieUpdate,
)
from recsys.features.ratings.model import Rating, RatingBase


async def create_movie(movie: MovieBase) -> Movie:
    async with postgres_connect() as conn:
        movie_db = Movie.model_validate(movie)
        conn.add(movie_db)
        await conn.commit()
        await conn.refresh(movie_db)
        return movie_db


async def get_movies(skip: int, limit: int) -> list[Movie]:
    async with postgres_connect() as conn:
        result = await conn.exec(select(Movie).offset(skip).limit(limit))
        movies = result.all()

        return movies


async def get_all_movies() -> list[Movie]:
    async with postgres_connect() as conn:
        result = await conn.exec(select(Movie))
        movies = result.all()

        return movies


async def get_movie(movie_id: int) -> Movie | None:
    async with postgres_connect() as conn:
        movie = await conn.get(Movie, movie_id)

        return movie


async def delete_movie(movie_id: int):
    async with postgres_connect() as conn:
        movie = await conn.get(Movie, movie_id)
        await conn.delete(movie)
        await conn.commit()


async def update_movie(movie_db: Movie, new_movie: MovieUpdate) -> Movie:
    async with postgres_connect() as conn:
        user_data = new_movie.model_dump(exclude_unset=True)
        movie_db.sqlmodel_update(user_data)
        conn.add(movie_db)
        await conn.commit()
        await conn.refresh(movie_db)
        return movie_db


async def create_movie_rating(
    movie: Movie, user_id: int,
    rating: RatingBase
) -> Rating:
    async with postgres_connect() as conn:
        rating_db = Rating.model_validate(rating)
        rating_db.movie_id = movie.id
        rating_db.user_id = user_id
        conn.add(rating_db)
        await conn.commit()
        await conn.refresh(rating_db)
        return rating_db


async def get_movie_ratings(movie_id: int):
    async with postgres_connect() as conn:
        query = select(Movie).options(selectinload(Movie.ratings))\
                .where(Movie.id == movie_id)
        result = await conn.exec(query)
        movie = result.first()

        return movie.ratings
