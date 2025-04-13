from typing import Annotated

from fastapi import APIRouter, Depends, status

from recsys.common.security import validate_user_authorization
from recsys.features.auth.application import get_current_user
from recsys.features.ratings import application
from recsys.features.ratings.model import RatingPublic, RatingUpdate
from recsys.features.users.model import User

router = APIRouter(
    prefix="/ratings",
    tags=["ratings"]
)


@router.get("/", status_code=status.HTTP_200_OK)
async def get_ratings(
    current_user: Annotated[User, Depends(get_current_user)],
    skip: int = 0, limit: int = 100
) -> list[RatingPublic]:
    ratings = await application.get_ratings(skip, limit)
    return ratings


@router.patch("/{rating_id}", status_code=status.HTTP_200_OK)
async def update_rating(
    rating_id: int, rating: RatingUpdate,
    current_user: Annotated[User, Depends(get_current_user)]
) -> RatingPublic:
    rating_db = await application.get_rating(rating_id)
    validate_user_authorization(current_user.id, rating_db.user_id)
    update_rating = await application.update_rating(rating_db, rating)
    return update_rating


@router.delete("/{rating_id}", status_code=status.HTTP_200_OK)
async def delete_rating(
    rating_id: int,
    current_user: Annotated[User, Depends(get_current_user)]
):
    rating_db = await application.get_rating(rating_id)
    validate_user_authorization(current_user.id, rating_db.user_id)
    await application.delete_rating(rating_db)

    return {"message": "Rating deleted"}
