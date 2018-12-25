
from api.config import Configs
from api.logger import logger


_engine = None


async def get_engine():
    from aiopg.sa import create_engine

    global _engine
    if not _engine:
        _engine = await create_engine(
                user=Configs['POSTGRES_USER'],
                database=Configs['POSTGRES_DATABASE'],
                host=Configs['POSTGRES_ADDRESS'],
                password=Configs['POSTGRES_PASSWORD']
            )
    return _engine


async def init_postgres():
    """
    Creates all tables that are represented by models in a Postgres database
    :return: None
    """
    from sqlalchemy.sql.ddl import CreateTable
    from api.pg_models import models

    engine = await get_engine()

    async with engine.acquire() as conn:
        for model in models:
            try:
                await conn.execute(CreateTable(model))
                logger.info(f'Table {model.name} has been successfully created')
            except Exception as e:
                logger.error(f'Encountered an error when creating a table %s: %s', model.name, e)


async def init_cassandra():
    """
    Creates 'movie' table in Cassandra keyspace and if there is no keyspace, it's also created
    :return: None
    """
    from cassandra.cqlengine import connection
    from cassandra.cqlengine.management import sync_table, create_keyspace_simple

    from api.cass_models import models

    connection.setup([Configs['CASSANDRA_HOST']], default_keyspace=Configs['CASSANDRA_KEYSPACE'])
    try:
        create_keyspace_simple(Configs['CASSANDRA_KEYSPACE'], replication_factor=1)
    except Exception as e:
        logger.error(f'Encountered an error when creating a keyspace %s: %s', Configs['CASSANDRA_KEYSPACE'], e)

    for model in models:
        try:
            sync_table(model)
        except Exception as e:
            logger.error(f'Encountered an error when creating a table movie: %s', e)






