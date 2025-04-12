from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import ARRAY
from sqlmodel import Field, SQLModel


class MovieBase(SQLModel):
    title: str
    genres: list[str]
    directors: list[str] | None
    actors: list[str] | None


class Movie(MovieBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    genres: list[str] = Field(sa_column=Column(ARRAY(String)))
    directors: list[str] | None = Field(default=None,
                                        sa_column=Column(ARRAY(String)))
    actors: list[str] | None = Field(default=None,
                                     sa_column=Column(ARRAY(String)))


class MoviePublic(MovieBase):
    id: int


class MovieUpdate(SQLModel):
    title: str | None = None
    genres: list[str] | None = None
    directors: list[str] | None = None
    actors: list[str] | None = None
