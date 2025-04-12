from sqlmodel import SQLModel, Field


class RatingBase(SQLModel):
    rating: int


class Rating(RatingBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_id: int | None = Field(default=None, foreign_key="user.id")
    movie_id: int | None = Field(default=None, foreign_key="movie.id")


class RatingPublic(RatingBase):
    id: int
    user_id: int
    movie_id: int


class RatingUpdate(SQLModel):
    rating: int | None = None
