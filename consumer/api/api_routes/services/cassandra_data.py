"""
    Module with helping functions for api to retrieve data from Cassandra database
"""

import uuid

from cassandra.cluster import Cluster
from cassandra.query import SimpleStatement, ConsistencyLevel

from api.config import Configs
from api.logger import logger


async def insert_movie(movie):
    session = None

    for i in range(Configs['CASSANDRA_RETRIES']):
        try:
            cluster = Cluster()
            session = cluster.connect(Configs['CASSANDRA_KEYSPACE'])
            break
        except Exception as e:
            logger.error("Couldn't connect to Cassandra database, try again in %s seconds: %s",
                         Configs['CASSANDRA_RETRY_TIME'], e)
            raise ConnectionError("Couldn't connect to Cassandra database")

    try:
        query = SimpleStatement(f"""
            INSERT INTO movie(id, title, release_date)
            VALUES(%(i)s, %(t)s, %(d)s)
        """, consistency_level=ConsistencyLevel.ONE)
        session.execute(query, {'i': uuid.uuid4(), 't': movie['title'], 'd': movie['release_date']})
    except Exception as e:
        logger.critical("Couldn't insert a new value into Cassandra database %s", e)
