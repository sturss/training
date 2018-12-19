
from api.models import models
from api.config import Configs


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
                    print(f'created table {model.name}')
                except Exception as ex:
                    print(ex)


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
        print(e)

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
        print(e)





