import asyncio

from api.forms import MovieForm
from api.config import Configs
from api.logger import logger

if Configs['DATA_STORAGE'] == 'POSTGRES':
    from api.api_routes.services.postgres_data import insert_movie
else:
    from api.api_routes.services.cassandra_data import insert_movie


def movie_call_back(message):
    data, errors = MovieForm().loads(message.value)
    if errors:
        logger.error("Consumer received message with incorrect format %s", data)
    else:
        loop = asyncio.get_event_loop()
        loop.create_task(insert_movie(data))
