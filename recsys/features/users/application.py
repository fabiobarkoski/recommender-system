import logging
import os

import pandas as pd
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError

from recsys.common import security
from recsys.features.movies.repository import get_all_movies, get_movie
from recsys.features.users import repository
from recsys.features.users.model import (
    FavoriteActorBase,
    FavoriteDirectorBase,
    User,
    UserCreate,
    UserPublic,
    UserUpdate,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def get_users(skip: int, limit: int) -> list[UserPublic]:
    users = await repository.get_users(skip, limit)
    return users


async def get_user(user_id: int) -> User:
    user = await repository.get_user(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="User not found")

    return user


async def create_user(user: UserCreate) -> UserPublic:
    user.password = security.get_password_hash(user.password)
    created_user = await repository.create_user(user)

    if isinstance(created_user, IntegrityError):
        if getattr(created_user.orig, "pgcode") == "23505":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    return created_user


async def delete_user(user_id: int):
    user_db = await get_user(user_id)
    await repository.delete_user(user_db)


async def update_user(user_id: int, user: UserUpdate) -> UserPublic:
    user_db = await get_user(user_id)
    if user.password:
        user.password = security.get_password_hash(user.password)
    updated_user = await repository.update_user(user_db, user)
    return updated_user


async def get_favorite_actors(user_id: int):
    favorite_actors = await repository.get_favorite_actors(user_id)
    return favorite_actors


async def post_favorite_actor(user_id: int, favorite_actor: FavoriteActorBase):
    created_favorite_actor = await repository.create_favorite_actor(
        user_id,
        favorite_actor
    )
    return created_favorite_actor


async def get_favorite_directors(user_id: int):
    favorite_directors = await repository.get_favorite_directors(user_id)
    return favorite_directors


async def post_favorite_director(
    user_id: int,
    favorite_director: FavoriteDirectorBase
):
    created_favorite_director = await repository.create_favorite_director(
        user_id,
        favorite_director
    )
    return created_favorite_director


async def get_ratings(user_id: int):
    ratings = await repository.get_ratings(user_id)

    return ratings


def get_favorites_values(favorites) -> list[str]:
    return [favorite.model_dump()["name"] for favorite in favorites]


async def get_user_infos(
    user_id: int
) -> tuple[pd.DataFrame, list[str], list[str]]:
    ratings = await get_ratings(user_id)
    ratings_df = pd.DataFrame([rating for rating in ratings])
    ratings_df = ratings_df.drop(columns=[
                                     "genres",
                                     "actors",
                                     "directors"
                                 ])

    favorite_actors = get_favorites_values(
        await repository.get_favorite_actors(user_id)
    )
    favorite_directors = get_favorites_values(
        await repository.get_favorite_directors(user_id)
    )

    return ratings_df, favorite_actors, favorite_directors


def generate_favorites_df(
    base_df: pd.DataFrame,
    favorites: list[str], name: str
) -> pd.DataFrame:
    favorites_rows = []

    for _, row in base_df.iterrows():
        favorites_flags = {}
        if row[name]:
            for value in row[name]:
                if value in favorites:
                    favorites_flags[value.strip()] = 1
                else:
                    favorites_flags[value.strip()] = 0
        favorites_rows.append(favorites_flags)

    favorites_df = pd.DataFrame(favorites_rows, index=base_df.index)
    result_df = pd.concat([base_df, favorites_df], axis=1).fillna(0)

    return result_df


def generate_df(base_df: pd.DataFrame, name: str) -> pd.DataFrame:
    values_rows = []

    for _, row in base_df.iterrows():
        values_flags = {}
        if row[name]:
            for value in row[name]:
                values_flags[value.strip()] = 1
        values_rows.append(values_flags)

    # Create a DataFrame with the same index and 1s for directors
    values_df = pd.DataFrame(values_rows, index=base_df.index)

    # Combine original DataFrame with the new one
    result_df = pd.concat([base_df, values_df], axis=1).fillna(0)

    return result_df


async def generate_user_profile(
    genres_df: pd.DataFrame,
    actors_df: pd.DataFrame,
    directors_df: pd.DataFrame,
    user_ratings: pd.DataFrame
) -> pd.DataFrame:
    genres_ratings = genres_df[
        genres_df["title"].isin(user_ratings["title"])
    ]
    actors_ratings = actors_df[
        actors_df["title"].isin(user_ratings["title"])
    ]
    directors_ratings = directors_df[
        directors_df["title"].isin(user_ratings["title"])
    ]

    user_genres = pd.merge(user_ratings, genres_ratings)
    user_actors = pd.merge(user_ratings, actors_ratings)
    user_directors = pd.merge(user_ratings, directors_ratings)

    columns_to_drop = [
        "title", "actors", "directors", "id", "rating", "genres",
        "id_x", "actors_x", "genres_x", "directors_x", "rating_x",
        "id_y", "actors_y", "genres_y", "directors_y", "rating_y"
    ]

    final_df = user_genres.merge(user_actors, on="title")\
                          .merge(user_directors, on="title")
    final_df = final_df.drop(columns=columns_to_drop)

    user_profile = final_df.T.dot(user_ratings.rating)

    return user_profile


def just_movies_genres(
    genres_df: pd.DataFrame,
    actors_df: pd.DataFrame,
    directors_df: pd.DataFrame
) -> pd.DataFrame:
    movies_and_genres = genres_df.merge(actors_df, on="title")\
                        .merge(directors_df, on="title")

    columns_to_drop = [
        "title", "actors", "directors", "genres",
        "id_x", "actors_x", "directors_x", "genres_x",
        "id_y", "actors_y", "directors_y", "genres_y"
    ]

    movies_and_genres = movies_and_genres.drop(columns=columns_to_drop)
    movies_and_genres = movies_and_genres.set_index(movies_and_genres.id)
    movies_and_genres = movies_and_genres.drop(columns=["id"])

    return movies_and_genres


def remove_watcheds_and_sort_recommendations(
    user_profile: pd.DataFrame,
    user_ratings_df: pd.DataFrame,
    genres_df: pd.DataFrame,
    just_movies_and_genres: pd.DataFrame
) -> list[int]:
    watcheds = genres_df[genres_df["title"].isin(user_ratings_df["title"])]

    recommendations = (
        just_movies_and_genres.dot(user_profile)
    ) / user_profile.sum()
    recommendations = recommendations[
        ~recommendations.index.isin(watcheds["id"])
    ].dropna()

    sorted_recommendations = recommendations.sort_values(ascending=False)
    top_recommendations = sorted_recommendations.index[
        :int(os.getenv("TOP_N"))
    ].tolist()

    return top_recommendations


async def generate_recommendation(
    user_id: int
) -> list[dict[str, str]]:
    user_ratings_df, favorite_actors, favorite_directors = await get_user_infos(
        user_id
    )

    movies = await get_all_movies()
    base_df = pd.DataFrame([movie.model_dump() for movie in movies])

    genres_df = generate_df(base_df, "genres")
    actors_df = generate_favorites_df(
        base_df, favorite_actors, "actors"
    )
    directors_df = generate_favorites_df(
        base_df, favorite_directors, "directors"
    )

    user_profile = await generate_user_profile(genres_df, actors_df,
                                               directors_df, user_ratings_df)
    logger.info(
        f"User Profile:\n{user_profile.sort_values(ascending=False).head(20)}"
    )

    just_movies_and_genres = just_movies_genres(genres_df, actors_df,
                                                directors_df)

    top_recommendations = remove_watcheds_and_sort_recommendations(
        user_profile,
        user_ratings_df,
        genres_df,
        just_movies_and_genres
    )

    recommended_movies = []
    for i in top_recommendations:
        movie = await get_movie(i)
        recommended_movies.append(movie)

    return recommended_movies


async def user_recommendation(user_id: int):
    recommendations = repository.get_recommendations(user_id)

    if not recommendations:
        recommendations = await generate_recommendation(user_id)

        repository.store_recommendations(user_id, recommendations)

    return recommendations
