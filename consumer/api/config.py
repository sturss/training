"""
    Module with application configurations
"""
import os

docker = os.environ.get('DOCKER', None)

Configs = {
    'POSTGRES_USER': os.environ.get('POSTGRES_USER') or 'admin',
    'POSTGRES_PASSWORD': os.environ.get('POSTGRES_PASSWORD') or 'admin',
    'POSTGRES_DATABASE': os.environ.get('POSTGRES_DATABASE') or 'movies',
    'OFFSET_STORAGE': os.environ.get('OFFSET_STORAGE') or 'REDIS',
    'DATA_STORAGE': os.environ.get('DATA_STORAGE') or 'POSTGRES',
    'ZOOKEEPER_PORT': os.environ.get('ZOOKEEPER_PORT') or 2181,
    'REDIS_PORT': os.environ.get('REDIS_PORT') or 6379,
    'CASSANDRA_KEYSPACE': os.environ.get('CASSANDRA_KEYSPACE') or 'movies',
    'CASSANDRA_RETRIES': os.environ.get('CASSANDRA_RETRIES') or 3,
    'CASSANDRA_RETRY_TIME': os.environ.get('CASSANDRA_RETRY_TIME') or 5
}

if not docker:
    Configs.update({
        'POSTGRES_ADDRESS': os.environ.get('POSTGRES_ADDRESS') or 'localhost',
        'KAFKA_SERVERS': os.environ.get('KAFKA_SERVERS') or 'localhost:9092',
        'ZOOKEEPER_HOST': os.environ.get('ZOOKEEPER_HOST') or 'localhost',
        'REDIS_HOST': os.environ.get('ZOOKEEPER_HOST') or 'localhost',
        'CASSANDRA_HOST': os.environ.get('CASSANDRA_HOST') or 'localhost',

    })
else:
    Configs.update({
        'POSTGRES_ADDRESS': os.environ.get('POSTGRES_ADDRESS') or 'postgres',
        'KAFKA_SERVERS': os.environ.get('KAFKA_SERVERS') or 'kafka:9092',
        'ZOOKEEPER_HOST': os.environ.get('ZOOKEEPER_HOST') or 'zookeeper',
        'REDIS_HOST': os.environ.get('REDIS_HOST') or 'redis',
        'CASSANDRA_HOST': os.environ.get('CASSANDRA_HOST') or 'cassandra',
    })

