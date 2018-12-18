import os

docker = os.environ.get('DOCKER', None)

if not docker:
    Configs = {
        'DATABASE_ADDRESS': 'localhost',
        'DATABASE_USER': 'admin',
        'DATABASE_PASSWORD': 'admin',
        'DATABASE_NAME': 'movies',

        'KAFKA_SERVER': 'localhost:9092',

        'OFFSET_STORAGE': 'ZOOKEEPER',
        'DATA_STORAGE': 'CASSANDRA',

        'ZOOKEEPER_HOST': 'localhost',
        'ZOOKEEPER_PORT': 2181,

        'REDIS_HOST': 'localhost',
        'REDIS_PORT': 6379,

        'CASSANDRA_HOST': 'localhost',
        'CASSANDRA_KEYSPACE': 'movies',
    }
else:
    Configs = {
        'DATABASE_ADDRESS': 'postgres',
        'DATABASE_USER': 'admin',
        'DATABASE_PASSWORD': 'admin',
        'DATABASE_NAME': 'movies',

        'KAFKA_SERVERS': ['kafka:9092'],

        'OFFSET_STORAGE': 'ZOOKEEPER',
        'DATA_STORAGE': 'CASSANDRA',

        'ZOOKEEPER_HOST': 'zookeeper',
        'ZOOKEEPER_PORT': 2181,

        'REDIS_HOST': 'redis',
        'REDIS_PORT': 6379,

        'CASSANDRA_HOST': 'cassandra',
        'CASSANDRA_KEYSPACE': 'movies',
    }

