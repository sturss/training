import uuid

from cassandra.cluster import Cluster
from cassandra.query import SimpleStatement, ConsistencyLevel

from api.config import Configs


async def insert_movie(movie):
    cluster = Cluster()
    session = cluster.connect(Configs['CASSANDRA_KEYSPACE'])

    try:
        query = SimpleStatement(f"""
            INSERT INTO movie(id, title, release_date)
            VALUES(%(i)s, %(t)s, %(d)s)
        """, consistency_level=ConsistencyLevel.ONE)
        session.execute(query, {'i': uuid.uuid4(), 't': movie['title'], 'd': movie['release_date']})
        print(f'successfully inserted {movie}')
    except Exception as e:
        print(e)
