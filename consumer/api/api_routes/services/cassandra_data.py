"""
    Module with helping functions for api to retrieve data from Cassandra database
"""

import asyncio
import uuid

from api.config import Configs
from api.logger import logger

from cassandra.cqlengine import connection


def check_connection(c):
    def decorate_function(f):
        async def wrapper(*args, **kwargs):
            if not connection.session:
                await c()
            return await f(*args, **kwargs)
        return wrapper
    return decorate_function


async def connect():
    """
    Blocking call for setting up connection with Cassandra
    :return: None
    """
    logger.info("Establishing connection with Cassandra")
    for i in range(Configs['CASSANDRA_CONNECTION_RETRIES']):
        try:
            connection.setup([Configs['CASSANDRA_ADDRESS']], default_keyspace=Configs['CASSANDRA_KEYSPACE'])
            logger.info("Connection with Cassandra has been established successfully")
            break
        except Exception as e:
            logger.warning("Couldn't connect to Cassandra, another try in %s seconds: %s",
                           Configs['CASSANDRA_CONNECTION_TIMEOUT'], e)
            await asyncio.sleep(Configs['CASSANDRA_CONNECTION_TIMEOUT'])
    else:
        logger.critical("Couldn't connect to Cassandra, check your settings and try again."
                        " (Consider increasing number of retries)")


@check_connection(connect)
async def insert_movie(movie):
    try:
        insert_query = f"""
                INSERT INTO {Configs['CASSANDRA_KEYSPACE']}."movie" (id, title, release_date) 
                VALUES (%s, %s, %s)
            """
        connection.session.execute_async(insert_query, (uuid.uuid4(), movie['title'], movie['release_date'])).result()
    except Exception as e:
        logger.critical("Couldn't insert a new value into Cassandra database %s", e)


@check_connection(connect)
async def get_movies_count():
    try:
        count_query = f'SELECT COUNT(*) FROM {Configs["CASSANDRA_KEYSPACE"]}."movie"'
        result = connection.session.execute_async(count_query).result()
        return result[0]['count']
    except Exception as e:
        logger.error("Error when making a query in Cassandra: %e", e)
