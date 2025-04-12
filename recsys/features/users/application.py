import os
import logging

import pandas as pd
from fastapi import HTTPException, status

from recsys.common import security
from recsys.features.users import repository
from recsys.features.movies.repository import get_movies
from recsys.features.users.model import User, UserCreate, UserPublic, UserUpdate

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def get_users() -> list[UserPublic]:
    users = await repository.get_users()
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


async def get_ratings(user_id: int) -> dict[str, str]:
    ratings = await repository.get_ratings(user_id)

    return ratings


def generate_genres_df(base_df):
    genres_df = base_df.copy(deep=True)
    idx = []
    for i, row in base_df.iterrows():
        idx.append(i)
        genres = row["genres"]
        for genre in genres:
            genres_df.at[i, genre.strip()] = 1
    genres_df = genres_df.fillna(0)

    return genres_df


def generate_actors_df(base_df):
    actor_rows = []

    for _, row in base_df.iterrows():
        actor_flags = {}
        if row["actors"]:
            for actor in row["actors"]:
                actor_flags[actor.strip()] = 1
        actor_rows.append(actor_flags)

    # Create a DataFrame with the same index and 1s for directors
    actors_df = pd.DataFrame(actor_rows, index=base_df.index)

    # Combine original DataFrame with the new one
    result_df = pd.concat([base_df, actors_df], axis=1).fillna(0)

    return result_df


def generate_directors_df(base_df):
    director_rows = []

    for _, row in base_df.iterrows():
        director_flags = {}
        if row["directors"]:
            for director in row["directors"]:
                director_flags[director.strip()] = 1
        director_rows.append(director_flags)

    # Create a DataFrame with the same index and 1s for directors
    directors_df = pd.DataFrame(director_rows, index=base_df.index)

    # Combine original DataFrame with the new one
    result_df = pd.concat([base_df, directors_df], axis=1).fillna(0)

    return result_df


async def generate_user_profile(user_id: int, genres_df, actors_df, directors_df, user_ratings):

    genres_ratings = genres_df[genres_df["title"].isin(user_ratings["title"])]
    actors_ratings = actors_df[actors_df["title"].isin(user_ratings["title"])]
    directors_ratings = directors_df[directors_df["title"].isin(user_ratings["title"])]

    user_genres = pd.merge(user_ratings, genres_ratings)
    user_actors = pd.merge(user_ratings, actors_ratings)
    user_directors = pd.merge(user_ratings, directors_ratings)

    dfzao = user_genres.merge(user_actors,on="title").merge(user_directors,on="title")
    dfzao = dfzao.drop(columns=[
                             "title", "actors", "directors", "id", "rating", "genres",
                             "id_x", "actors_x", "genres_x", "directors_x", "rating_x",
                             "id_y", "actors_y", "genres_y", "directors_y", "rating_y"
                             ])

    user_profile = dfzao.T.dot(user_ratings.rating)

    return user_profile


def just_movies_genres(genres_df, actors_df, directors_df):
    movies_and_genres = genres_df.merge(actors_df, on="title").merge(directors_df, on="title")
    movies_and_genres = movies_and_genres.drop(columns=[
                                               "title", "actors", "directors", "genres",
                                               "id_x", "actors_x", "directors_x", "genres_x",
                                               "id_y", "actors_y", "directors_y", "genres_y"
                                           ])
    movies_and_genres = movies_and_genres.set_index(movies_and_genres.id)
    movies_and_genres = movies_and_genres.drop(columns=["id"])

    return movies_and_genres


async def generate_recommendation(user_id: int, top_n: int = 20) -> list[dict[str, str]]:
    movies = await get_movies()
    df = pd.DataFrame([movie.dict() for movie in movies])
    ratings = await get_ratings(user_id)
    user_ratings_df = pd.DataFrame([rating for rating in ratings])
    user_ratings_df = user_ratings_df.drop(columns=["genres", "actors", "directors"])

    genres_df = generate_genres_df(df)
    actors_df = generate_actors_df(df)
    directors_df = generate_directors_df(df)

    user_profile = await generate_user_profile(user_id, genres_df,
                                               actors_df, directors_df,
                                               user_ratings_df)
    logger.info(f"User Profile:\n{user_profile}")

    just_movies_and_genres = just_movies_genres(genres_df, actors_df, directors_df)

    abloba = genres_df[genres_df["title"].isin(user_ratings_df["title"])]

    recommendations = (just_movies_and_genres.dot(user_profile)) / user_profile.sum()
    recommendations = recommendations[~recommendations.index.isin(abloba["id"])].dropna()
    sorted_recommendations = recommendations.sort_values(ascending=False)
    top_recommendations = sorted_recommendations.index[:top_n].tolist()
    recommended_movies = []
    logger.info(f"TOP {top_n} Movies")
    for i in top_recommendations:
        movie = await repository.get_movie(i)
        recommended_movies.append(movie)

    return recommended_movies


async def user_recommendation(user_id: int):
    recommendations = repository.get_recommendations(user_id)

    if not recommendations:
        recommendations = await generate_recommendation(user_id, os.getenv("TOP_N"))

        repository.store_recommendations(user_id, recommendations)

    return recommendations
