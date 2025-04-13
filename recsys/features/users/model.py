from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from recsys.features.ratings.model import Rating


class UserBase(SQLModel):
    name: str
    email: str


class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    email: str = Field(index=True, sa_column_kwargs={"unique": True})
    password: str

    favorite_actors: list["FavoriteActor"] = Relationship(
        back_populates="user"
    )
    favorite_directors: list["FavoriteDirector"] = Relationship(
        back_populates="user"
    )
    ratings: list["Rating"] = Relationship(back_populates="user")


class UserPublic(UserBase):
    id: int


class UserCreate(UserBase):
    password: str


class UserUpdate(SQLModel):
    name: str | None = None
    password: str | None = None


class FavoriteActorBase(SQLModel):
    name: str


class FavoriteActor(FavoriteActorBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_id: int | None = Field(default=None, foreign_key="user.id")
    name: str = Field(sa_column_kwargs={"unique": True})

    user: User | None = Relationship(back_populates="favorite_actors")


class FavoriteActorPublic(FavoriteActorBase):
    id: int


class FavoriteDirectorBase(SQLModel):
    name: str


class FavoriteDirector(FavoriteDirectorBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_id: int | None = Field(default=None, foreign_key="user.id")
    name: str = Field(sa_column_kwargs={"unique": True})

    user: User | None = Relationship(back_populates="favorite_directors")


class FavoriteDirectorPublic(FavoriteActorBase):
    id: int
