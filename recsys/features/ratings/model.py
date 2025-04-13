from sqlmodel import Field, Relationship, SQLModel

from recsys.features.movies.model import Movie
from recsys.features.users.model import User


class RatingBase(SQLModel):
    rating: int


class Rating(RatingBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_id: int | None = Field(default=None,
                                foreign_key="user.id",
                                unique=True)
    movie_id: int | None = Field(default=None,
                                 foreign_key="movie.id",
                                 unique=True)

    user: User | None = Relationship(back_populates="ratings")
    movie: Movie | None = Relationship(back_populates="ratings")


class RatingPublic(RatingBase):
    id: int
    user_id: int
    movie_id: int


class RatingUpdate(SQLModel):
    rating: int | None = None
