import ast
import json
import asyncio

import pandas as pd


from recsys.features.movies.model import Movie
from recsys.common.database import postgres_connect
from recsys.features.movies.repository import create_movie

df = pd.read_csv("./scripts/movies_dataset.csv")

df = df.drop(columns=["Unnamed: 0"])

values = df.to_json(orient="records")


def to_list(value: str) -> list[str]:
    if value:
        return ast.literal_eval(value)
    return None


def treat_values(values_list: list[str]) -> list[str]:
    if values_list:
        return [v.strip() for v in values_list]
    return None


async def batch_movie(movies):
    async with postgres_connect() as conn:
        for movie in movies:
            genres = treat_values(to_list(movie["genres"]))
            actors = treat_values(to_list(movie["actors"]))
            directors = treat_values(to_list(movie["directors"]))

            movie_obj = Movie(
                title=movie["title"],
                genres=genres,
                actors=actors,
                directors=directors
            )

            conn.add(movie_obj)
        await conn.commit()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(batch_movie(json.loads(values)))
    loop.close()
