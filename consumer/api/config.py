import os

docker = os.environ.get('DOCKER', None)


Configs = {}

if not docker:
    Configs = {
        'POSTGRES_ADDRESS': os.environ.get('POSTGRES_ADDRESS') or 'localhost',
        'POSTGRES_USER': os.environ.get('POSTGRES_USER') or 'admin',
        'POSTGRES_PASSWORD': os.environ.get('POSTGRES_PASSWORD') or 'admin',
        'POSTGRES_DATABASE': os.environ.get('POSTGRES_DATABASE') or 'movies',

        'KAFKA_SERVER': os.environ.get('KAFKA_SERVER') or 'localhost:9092',

        'OFFSET_STORAGE': os.environ.get('OFFSET_STORAGE') or 'REDIS',
        'DATA_STORAGE': os.environ.get('DATA_STORAGE') or 'POSTGRES',

        'ZOOKEEPER_HOST': os.environ.get('ZOOKEEPER_HOST') or 'localhost',
        'ZOOKEEPER_PORT': os.environ.get('ZOOKEEPER_PORT') or 2181,

        'REDIS_HOST': os.environ.get('ZOOKEEPER_HOST') or 'localhost',
        'REDIS_PORT': os.environ.get('REDIS_PORT') or 6379,

        'CASSANDRA_HOST': os.environ.get('CASSANDRA_HOST') or 'localhost',
        'CASSANDRA_KEYSPACE': os.environ.get('CASSANDRA_KEYSPACE') or 'movies',
    }
else:
    Configs = {
        'POSTGRES_ADDRESS': os.environ.get('POSTGRES_ADDRESS') or 'postgres',
        'POSTGRES_USER': os.environ.get('POSTGRES_USER') or 'admin',
        'POSTGRES_PASSWORD': os.environ.get('POSTGRES_PASSWORD') or 'admin',
        'POSTGRES_DATABASE': os.environ.get('POSTGRES_DATABASE') or 'movies',

        'KAFKA_SERVERS': os.environ.get('KAFKA_SERVERS') or 'kafka:9092',

        'OFFSET_STORAGE': os.environ.get('OFFSET_STORAGE') or 'ZOOKEEPER',
        'DATA_STORAGE': os.environ.get('DATA_STORAGE') or 'POSTGRES',

        'ZOOKEEPER_HOST': os.environ.get('ZOOKEEPER_HOST') or 'zookeeper',
        'ZOOKEEPER_PORT': os.environ.get('ZOOKEEPER_PORT') or 2181,

        'REDIS_HOST': os.environ.get('REDIS_HOST') or 'redis',
        'REDIS_PORT': os.environ.get('REDIS_PORT') or 6379,

        'CASSANDRA_HOST': os.environ.get('CASSANDRA_HOST') or 'cassandra',
        'CASSANDRA_KEYSPACE': os.environ.get('CASSANDRA_KEYSPACE') or 'movies',
    }

