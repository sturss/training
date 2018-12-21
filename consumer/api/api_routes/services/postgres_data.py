"""
    Module with helping functions for api to retrieve data from Postgres database
"""

from aiopg.sa import create_engine

from api.config import Configs
from api.pg_models import Movie


async def insert_movie(movie):
    async with create_engine(
        user=Configs['POSTGRES_USER'],
        database=Configs['POSTGRES_DATABASE'],
        host=Configs['POSTGRES_ADDRESS'],
        password=Configs['POSTGRES_PASSWORD']
    ) as engine:
        async with engine.acquire() as conn:
            async with conn.begin():
                await conn.execute(Movie.insert().values(movie))


async def get_movies_count():
    async with create_engine(
        user=Configs['POSTGRES_USER'],
        database=Configs['POSTGRES_DATABASE'],
        host=Configs['POSTGRES_ADDRESS'],
        password=Configs['POSTGRES_PASSWORD']
    ) as engine:
        async with engine.acquire() as conn:
            async with conn.execute(Movie.select()) as cur:
                return cur.rowcount


