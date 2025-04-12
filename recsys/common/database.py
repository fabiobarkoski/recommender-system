import os
from contextlib import contextmanager, asynccontextmanager

from redis import Redis
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

load_dotenv()
engine = create_async_engine(os.getenv("POSTGRES_URL"))


def create_db():
    SQLModel.metadata.create_all(engine)


@contextmanager
def redis_connection():
    with Redis(host=os.getenv("REDIS_HOST"), port=os.getenv("REDIS_POST"),
               password=os.getenv("REDIS_PASSWORD"), decode_responses=True) as r:
        yield r


@asynccontextmanager
async def postgres_connect() -> AsyncSession:
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session


if __name__ == "__main__":
    create_db()
