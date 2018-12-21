"""
    Module with helping functions for api to retrieve data from Cassandra database
"""

import uuid

from api.config import Configs
from api.logger import logger

from cassandra.cqlengine import connection
from api.cass_models import Movie

connection.setup([Configs['CASSANDRA_HOST']], default_keyspace=Configs['CASSANDRA_KEYSPACE'])


async def insert_movie(movie):
    try:
        Movie.create(id=uuid.uuid4(), title=movie['title'], release_date=movie['release_date'])
    except Exception as e:
        logger.critical("Couldn't insert a new value into Cassandra database %s", e)


async def get_movies_count():
    try:
        return Movie.objects.count()
    except Exception as e:
        logger.error("Error when making a query in Cassandra: %e", e)
