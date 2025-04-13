from sqlmodel import select

from recsys.common.database import postgres_connect
from recsys.features.ratings.model import Rating, RatingUpdate


async def get_rating(rating_id: int) -> Rating | None:
    async with postgres_connect() as conn:
        rating = await conn.get(Rating, rating_id)
        return rating


async def get_ratings(skip: int, limit: int):
    async with postgres_connect() as conn:
        result = await conn.exec(select(Rating).offset(skip).limit(limit))
        ratings = result.all()

        return ratings


async def update_rating(rating_db: Rating, new_rating: RatingUpdate) -> Rating:
    async with postgres_connect() as conn:
        rating_data = new_rating.model_dump(exclude_unset=True)
        rating_db.sqlmodel_update(rating_data)

        conn.add(rating_db)
        await conn.commit()
        await conn.refresh(rating_db)
        return rating_db


async def delete_rating(rating: Rating):
    async with postgres_connect() as conn:
        await conn.delete(rating)
        await conn.commit()
