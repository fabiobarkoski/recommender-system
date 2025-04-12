from sqlmodel import Field, SQLModel


class UserBase(SQLModel):
    name: str
    email: str


class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    email: str = Field(unique=True)
    password: str


class UserPublic(UserBase):
    id: int


class UserCreate(UserBase):
    password: str


class UserUpdate(SQLModel):
    name: str | None = None
    password: str | None = None
