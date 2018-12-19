
from api.models import models
from api.config import Configs
from api.logger import logger


async def init_postgres():
    from aiopg.sa import create_engine
    from sqlalchemy.sql.ddl import CreateTable

    async with create_engine(
        user=Configs['POSTGRES_USER'],
        database=Configs['POSTGRES_DATABASE'],
        host=Configs['POSTGRES_ADDRESS'],
        password=Configs['POSTGRES_PASSWORD']
    ) as engine:
        async with engine.acquire() as conn:
            for model in models:
                try:
                    await conn.execute(CreateTable(model))
                    logger.info(f'Table {model.name} has been successfully created')
                except Exception as e:
                    logger.error(f'Encountered an error when creating a table %s: %s', model.name, e)



async def init_cassandra():
    from cassandra.cluster import Cluster

    cluster = Cluster([Configs['CASSANDRA_HOST']])
    session = cluster.connect()
    try:
        session.execute(f"""
            CREATE KEYSPACE {Configs['CASSANDRA_KEYSPACE']}
            WITH replication={{'class': 'SimpleStrategy', 'replication_factor': 1 }}
        """)
    except Exception as e:
        logger.error(f'Encountered an error when creating a keyspace %s: %s', Configs['CASSANDRA_KEYSPACE'], e)

    try:
        session.set_keyspace(Configs['CASSANDRA_KEYSPACE'])
        session.execute(f"""
            CREATE TABLE movie(
                id UUID,
                title text,
                release_date date,
                PRIMARY KEY (id)
            )           
        """)
    except Exception as e:
        logger.error(f'Encountered an error when creating a table movie: %s', e)






