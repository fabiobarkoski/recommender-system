from typing import Annotated

from fastapi import APIRouter, Depends, status

from recsys.features.users.model import User
from recsys.features.ratings import application
from recsys.features.ratings.model import RatingPublic, RatingUpdate
from recsys.features.auth.application import get_current_user

router = APIRouter(
    prefix="/ratings",
    tags=["ratings"]
)


@router.get("/", status_code=status.HTTP_200_OK)
async def get_ratings() -> list[RatingPublic]:
    ratings = await application.get_ratings()
    return ratings


@router.patch("/{rating_id}", status_code=status.HTTP_200_OK)
async def update_rating(
    rating_id: int, rating: RatingUpdate,
    current_user: Annotated[User, Depends(get_current_user)]
) -> RatingPublic:
    update_rating = application.update_rating(rating_id, rating)
    return update_rating


@router.delete("/{rating_id}", status_code=status.HTTP_200_OK)
async def delete_rating(rating_id: int):
    await application.delete_rating(rating_id)

    return {"message": "Rating deleted!"}
