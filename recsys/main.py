from fastapi import FastAPI

from recsys.features.auth import routes as auth_router
from recsys.features.users import routes as user_router
from recsys.features.movies import routes as movie_router

app = FastAPI()

app.include_router(auth_router.router)
app.include_router(user_router.router)
app.include_router(movie_router.router)
