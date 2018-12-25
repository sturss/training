"""
    Module with helping functions for api to retrieve data from Cassandra database
"""

import uuid

from api.config import Configs
from api.logger import logger

from cassandra.cqlengine import connection

connection.setup([Configs['CASSANDRA_HOST']], default_keyspace=Configs['CASSANDRA_KEYSPACE'])


async def insert_movie(movie):
    try:
        insert_query = f"""
                INSERT INTO {Configs['CASSANDRA_KEYSPACE']}."movie" (id, title, release_date) 
                VALUES (%s, %s, %s)
            """
        connection.session.execute_async(insert_query, (uuid.uuid4(), movie['title'], movie['release_date'])).result()
    except Exception as e:
        logger.critical("Couldn't insert a new value into Cassandra database %s", e)


async def get_movies_count():
    try:
        count_query = f'SELECT COUNT(*) FROM {Configs["CASSANDRA_KEYSPACE"]}."movie"'
        result = connection.session.execute_async(count_query).result()
        return result[0]['count']
    except Exception as e:
        logger.error("Error when making a query in Cassandra: %e", e)
