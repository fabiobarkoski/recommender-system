from fastapi import HTTPException, status

from recsys.features.ratings import repository
from recsys.features.ratings.model import Rating, RatingPublic, RatingUpdate


async def get_rating(rating_id: int) -> Rating:
    rating = await repository.get_rating(rating_id)
    if not rating:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Rating not found"
        )

    return rating


async def get_ratings(skip: int, limit: int) -> list[RatingPublic]:
    ratings = await repository.get_ratings()
    return ratings


async def update_rating(
    rating_db: Rating,
    rating: RatingUpdate
) -> RatingPublic:
    updated_rating = await repository.update_rating(rating_db, rating)
    return updated_rating


async def delete_rating(rating: Rating):
    await repository.delete_rating(rating)
