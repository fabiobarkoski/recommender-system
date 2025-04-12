from sqlmodel import select

from recsys.common.database import postgres_connect
from recsys.features.ratings.model import Rating, RatingUpdate


async def get_rating(rating_id: int) -> Rating | None:
    with postgres_connect() as conn:
        rating = conn.get(rating_id)
        return rating


async def get_ratings():
    with postgres_connect() as conn:
        result = await conn.exec(select(Rating))
        ratings = result.all()

        return ratings


async def update_rating(rating_db: Rating, new_rating: RatingUpdate) -> Rating:
    with postgres_connect() as conn:
        rating_data = new_rating.model_dump(exclude_unset=True)
        rating_db.sqlmodel_update(rating_data)

        conn.add(rating_db)
        await conn.commit()
        await conn.refresh(rating_db)
        return rating_db


async def delete_rating(rating: Rating):
    with postgres_connect() as conn:
        await conn.delete(rating)
        await conn.commit()
