from aiopg.sa import create_engine

from api.config import Configs
from api.models import Movie


async def insert_movie(movie):
    async with create_engine(
        user=Configs['DATABASE_USER'],
        database=Configs['DATABASE_NAME'],
        host=Configs['DATABASE_ADDRESS'],
        password=Configs['DATABASE_PASSWORD']
    ) as engine:
        async with engine.acquire() as conn:
            async with conn.begin():
                await conn.execute(Movie.insert().values(movie))


async def get_movies(movie):
    async with create_engine(
        user=Configs['DATABASE_USER'],
        database=Configs['DATABASE_NAME'],
        host=Configs['DATABASE_ADDRESS'],
        password=Configs['DATABASE_PASSWORD']
    ) as engine:
        async with engine.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(Movie.select().values(movie))
                print(cur)


