import json

from sqlmodel import select

from recsys.features.movies.model import Movie
from recsys.features.ratings.model import Rating
from recsys.features.users.model import User, UserBase, UserUpdate
from recsys.common.database import redis_connection, postgres_connect


async def create_user(user: UserBase):
    async with postgres_connect() as conn:
        user_db = User.model_validate(user)
        conn.add(user_db)
        await conn.commit()
        await conn.refresh(user_db)
        return user_db


async def get_users() -> list[User]:
    async with postgres_connect() as conn:
        result = await conn.exec(select(User))
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


async def get_ratings(user_id: int):
    async with postgres_connect() as conn:
        query = select(
                       Movie.title, Movie.genres,
                       Movie.actors, Movie.directors,
                       Rating.rating
                   ).join(Movie).where(Rating.user_id == user_id)
        result = await conn.exec(query)
        ratings = result.all()

        ratings = [
            {
                "title": r[0], "genres": r[1],
                "actors": r[2], "directors": r[3], "rating": r[4]
            }
            for r in ratings
        ]

        return ratings


def store_recommendations(user_id: int, recommendations: dict[str, str]):
    recommendations_in_json = [r.dict() for r in recommendations]
    with redis_connection() as conn:
        conn.setex(f"{user_id}", 600, json.dumps(recommendations_in_json))


def get_recommendations(user_id: int) -> dict[str, str] | None:
    with redis_connection() as conn:
        result = conn.get(f"{user_id}")

        if result:
            recommendations_in_json = json.loads(result)
            recommendations = [Movie(**r) for r in recommendations_in_json]
            return recommendations

        return None
