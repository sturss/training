"""
    Module with helping functions for api to retrieve data from Postgres database
"""

from aiopg.sa import create_engine

from api.config import Configs
from api.pg_models import Movie

_engine = None


async def get_engine():
    global _engine
    if not _engine:
        _engine = await create_engine(
                user=Configs['POSTGRES_USER'],
                database=Configs['POSTGRES_DATABASE'],
                host=Configs['POSTGRES_ADDRESS'],
                password=Configs['POSTGRES_PASSWORD']
            )
    return _engine


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


