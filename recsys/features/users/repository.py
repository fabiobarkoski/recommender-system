import json
import os

from sqlalchemy.exc import IntegrityError
from sqlmodel import select

from recsys.common.database import postgres_connect, redis_connection
from recsys.features.movies.model import Movie
from recsys.features.ratings.model import Rating
from recsys.features.users.model import (
    FavoriteActor,
    FavoriteActorBase,
    FavoriteDirector,
    FavoriteDirectorBase,
    User,
    UserBase,
    UserUpdate,
)


async def create_user(user: UserBase):
    async with postgres_connect() as conn:
        user_db = User.model_validate(user)
        conn.add(user_db)
        try:
            await conn.commit()
            await conn.refresh(user_db)
            return user_db
        except IntegrityError as error:
            await conn.rollback()
            return error


async def get_users(skip: int, limit: int) -> list[User]:
    async with postgres_connect() as conn:
        result = await conn.exec(select(User).offset(skip).limit(limit))
        users = result.all()

        return users


async def get_user(user_id: int) -> User | None:
    async with postgres_connect() as conn:
        user = await conn.get(User, user_id)

    return user


async def get_user_by_email(email: str) -> User | None:
    async with postgres_connect() as conn:
        result = await conn.exec(select(User).where(User.email == email))
        user = result.first()
        return user


async def delete_user(user: User):
    async with postgres_connect() as conn:
        await conn.delete(user)
        await conn.commit()


async def update_user(user_db: User, new_user: UserUpdate) -> User:
    async with postgres_connect() as conn:
        user_data = new_user.model_dump(exclude_unset=True)
        user_db.sqlmodel_update(user_data)

        conn.add(user_db)
        await conn.commit()
        await conn.refresh(user_db)
        return user_db


async def create_favorite_actor(
    user_id: int,
    favorite_actor: FavoriteActorBase
) -> FavoriteActor:
    async with postgres_connect() as conn:
        favorite_actor_db = FavoriteActor.model_validate(
            {
                "user_id": user_id,
                **favorite_actor.dict()
            }
        )
        conn.add(favorite_actor_db)
        await conn.commit()
        await conn.refresh(favorite_actor_db)

        return favorite_actor_db


async def get_favorite_actors(user_id: int):
    async with postgres_connect() as conn:
        query = select(FavoriteActor).where(FavoriteActor.user_id == user_id)
        result = await conn.exec(query)
        favorite_actors = result.all()

        return favorite_actors


async def create_favorite_director(
    user_id: int,
    favorite_director: FavoriteDirectorBase
) -> FavoriteDirector:
    async with postgres_connect() as conn:
        favorite_director_db = FavoriteDirector.model_validate(
            {
                "user_id": user_id,
                **favorite_director.dict()
            }
        )
        conn.add(favorite_director_db)
        await conn.commit()
        await conn.refresh(favorite_director_db)

        return favorite_director_db


async def get_favorite_directors(user_id: int):
    async with postgres_connect() as conn:
        query = select(FavoriteDirector)\
                .where(FavoriteDirector.user_id == user_id)
        result = await conn.exec(query)
        favorite_directors = result.all()

        return favorite_directors


async def get_ratings(user_id: int):
    async with postgres_connect() as conn:
        query = select(
                       Movie.id, Movie.title,
                       Movie.genres, Movie.actors,
                       Movie.directors, Rating.rating
                   ).join(Movie).where(Rating.user_id == user_id)
        result = await conn.exec(query)
        ratings = result.all()

        ratings = [
            {
                "id": r[0], "title": r[1], "genres": r[2],
                "actors": r[3], "directors": r[4], "rating": r[5]
            }
            for r in ratings
        ]

        return ratings


def store_recommendations(user_id: int, recommendations: dict[str, str]):
    recommendations_in_json = [r.dict() for r in recommendations]
    with redis_connection() as conn:
        conn.setex(f"{user_id}", int(os.getenv("CACHE_TIME")),
                   json.dumps(recommendations_in_json))


def get_recommendations(user_id: int) -> dict[str, str] | None:
    with redis_connection() as conn:
        result = conn.get(f"{user_id}")

        if result:
            recommendations_in_json = json.loads(result)
            recommendations = [Movie(**r) for r in recommendations_in_json]
            return recommendations

        return None
