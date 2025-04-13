from typing import Annotated

from fastapi import APIRouter, Depends, status

from recsys.common.security import validate_user_authorization
from recsys.features.auth.application import get_current_user
from recsys.features.users import application
from recsys.features.users.model import (
    FavoriteActorBase,
    FavoriteDirectorBase,
    User,
    UserCreate,
    UserPublic,
    UserUpdate,
)

router = APIRouter(
    prefix="/users",
    tags=["users"]
)


@router.get("/", status_code=status.HTTP_200_OK)
async def get_users(
    current_user: Annotated[User, Depends(get_current_user)],
    skip: int = 0, limit: int = 100,
) -> list[UserPublic]:
    users = await application.get_users(skip, limit)
    return users


@router.post("/", status_code=status.HTTP_201_CREATED)
async def post_user(
    user: UserCreate,
) -> UserPublic:
    created_user = await application.create_user(user)
    return created_user


@router.get("/ratings", status_code=status.HTTP_200_OK)
async def get_user_ratings(
    current_user: Annotated[User, Depends(get_current_user)]
):
    ratings = await application.get_ratings(current_user.id)
    return ratings


@router.get("/recommendations", status_code=status.HTTP_200_OK)
async def get_user_recommendations(
    current_user: Annotated[User, Depends(get_current_user)]
):
    recommendations = await application.user_recommendation(current_user.id)
    return recommendations


@router.get("/favorites/actors", status_code=status.HTTP_200_OK)
async def get_favorite_actors(
    current_user: Annotated[User, Depends(get_current_user)]
):
    favorite_actors = await application.get_favorite_actors(current_user.id)
    return favorite_actors


@router.post("/favorites/actors", status_code=status.HTTP_201_CREATED)
async def post_favorite_actor(
    favorite_actor: FavoriteActorBase,
    current_user: Annotated[User, Depends(get_current_user)]
):
    created_favorite_actor = await application.post_favorite_actor(
        current_user.id,
        favorite_actor
    )
    return created_favorite_actor


@router.get("/favorites/directors", status_code=status.HTTP_200_OK)
async def get_favorite_directors(
    current_user: Annotated[User, Depends(get_current_user)]
):
    favorite_actors = await application.get_favorite_directors(current_user.id)
    return favorite_actors


@router.post("/favorites/directors", status_code=status.HTTP_201_CREATED)
async def post_favorite_director(
    favorite_director: FavoriteDirectorBase,
    current_user: Annotated[User, Depends(get_current_user)]
):
    created_favorite_director = await application.post_favorite_director(
        current_user.id,
        favorite_director
    )
    return created_favorite_director


@router.get("/{user_id}", status_code=status.HTTP_200_OK)
async def get_user(
    user_id: int,
    current_user: Annotated[User, Depends(get_current_user)]
) -> UserPublic:
    validate_user_authorization(current_user.id, user_id)
    user = await application.get_user(user_id)
    return user


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
    validate_user_authorization(current_user.id, user_id)
    await application.delete_user(user_id)

    return {"message": "User deleted"}
