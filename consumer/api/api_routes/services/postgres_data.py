"""
    Module with helping functions for api to retrieve data from Postgres database
"""

from common.database import get_engine
from api.pg_models import Movie


async def insert_movie(movie):
    engine = await get_engine()
    async with engine.acquire() as conn:
        async with conn.begin():
            await conn.execute(Movie.insert().values(movie))


async def get_movies_count():
    engine = await get_engine()
    async with engine.acquire() as conn:
        async with conn.execute(Movie.select()) as cur:
            return cur.rowcount


