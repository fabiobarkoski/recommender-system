from typing import Annotated

from fastapi import APIRouter, Depends, status

from recsys.features.users import application
from recsys.features.auth.application import get_current_user
from recsys.common.security import validate_user_authorization
from recsys.features.users.model import User, UserCreate, UserPublic, UserUpdate

router = APIRouter(
    prefix="/users",
    tags=["users"]
)


@router.get("/", status_code=status.HTTP_200_OK)
async def get_users() -> list[UserPublic]:
    users = await application.get_users()
    return users


@router.get("/{user_id}", status_code=status.HTTP_200_OK)
async def get_user(user_id: int) -> UserPublic:
    user = await application.get_user(user_id)
    return user


@router.post("/", status_code=status.HTTP_201_CREATED)
async def post_user(user: UserCreate) -> UserPublic:
    created_user = await application.create_user(user)
    return created_user


@router.patch("/{user_id}", status_code=status.HTTP_200_OK)
async def patch_user(
    user_id: int, user: UserUpdate,
    current_user: Annotated[User, Depends(get_current_user)]
) -> UserPublic:
    validate_user_authorization(current_user.id, user_id)
    updated_user = await application.update_user(user_id, user)
    return updated_user


@router.delete("/{user_id}", status_code=status.HTTP_200_OK)
async def delete_user(
    user_id: int,
    current_user: Annotated[User, Depends(get_current_user)]
) -> dict[str, str]:
    await application.delete_user(user_id)

    return {"message": "User deleted!"}


@router.get("/recommendations", status_code=status.HTTP_200_OK)
async def get_user_recommendations(
    current_user: Annotated[User, Depends(get_current_user)]
):
    recommendations = await application.user_recommendation(current_user.id)
    return recommendations


@router.get("/ratings", status_code=status.HTTP_200_OK)
async def get_user_ratings(
    current_user: Annotated[User, Depends(get_current_user)]
):
    ratings = await application.get_ratings(current_user.id)
    return ratings
