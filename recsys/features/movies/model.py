from typing import TYPE_CHECKING

from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import ARRAY
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from recsys.features.ratings.model import Rating


class MovieBase(SQLModel):
    title: str
    genres: list[str]
    actors: list[str] | None
    directors: list[str] | None


class Movie(MovieBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    genres: list[str] = Field(sa_column=Column(ARRAY(String)))
    actors: list[str] | None = Field(default=None,
                                     sa_column=Column(ARRAY(String)))
    directors: list[str] | None = Field(default=None,
                                        sa_column=Column(ARRAY(String)))

    ratings: list["Rating"] = Relationship(back_populates="movie")


class MoviePublic(MovieBase):
    id: int


class MovieUpdate(SQLModel):
    title: str | None = None
    genres: list[str] | None = None
    directors: list[str] | None = None
    actors: list[str] | None = None
