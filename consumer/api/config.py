"""
    Module with application configurations
"""
import os

docker = os.environ.get('DOCKER', None)

Configs = {
    'POSTGRES_ADDRESS': os.environ.get('POSTGRES_ADDRESS') or 'localhost',
    'POSTGRES_USER': os.environ.get('POSTGRES_USER') or 'admin',
    'POSTGRES_PASSWORD': os.environ.get('POSTGRES_PASSWORD') or 'admin',
    'POSTGRES_DATABASE': os.environ.get('POSTGRES_DATABASE') or 'movies',
    'POSTGRES_PORT': os.environ.get('POSTGRES_PORT') or 5432,

    'OFFSET_STORAGE': os.environ.get('OFFSET_STORAGE') or 'REDIS',
    'DATA_STORAGE': os.environ.get('DATA_STORAGE') or 'CASSANDRA',

    'REDIS_ADDRESS': os.environ.get('ZOOKEEPER_HOST') or 'localhost',
    'REDIS_PORT': os.environ.get('REDIS_PORT') or 6379,
    'REDIS_CONNECTION_RETRIES': os.environ.get('REDIS_CONNECTION_RETRIES') or 2,
    'REDIS_CONNECTION_TIMEOUT': os.environ.get('REDIS_CONNECTION_TIMEOUT') or 3,

    'ZOOKEEPER_ADDRESS': os.environ.get('ZOOKEEPER_HOST') or 'localhost',
    'ZOOKEEPER_PORT': os.environ.get('ZOOKEEPER_PORT') or 2181,
    'ZOOKEEPER_CONNECTION_RETRIES': os.environ.get('ZOOKEEPER_CONNECTION_RETRIES') or 3,
    'ZOOKEEPER_CONNECTION_TIMEOUT': os.environ.get('ZOOKEEPER_CONNECTION_TIMEOUT') or 3,

    'CASSANDRA_ADDRESS': os.environ.get('CASSANDRA_HOST') or 'localhost',
    'CASSANDRA_KEYSPACE': os.environ.get('CASSANDRA_KEYSPACE') or 'movies',
    'CASSANDRA_CONNECTION_RETRIES': os.environ.get('CASSANDRA_CONNECTION_RETRIES') or 5,
    'CASSANDRA_CONNECTION_TIMEOUT': os.environ.get('CASSANDRA_CONNECTION_TIMEOUT') or 5,

    'KAFKA_ADDRESS': os.environ.get('KAFKA_SERVERS') or 'localhost',
    'KAFKA_PORT': os.environ.get('KAFKA_PORT') or 9092,
    'KAFKA_COMMIT_SECONDS_INTERVAL': os.environ.get('KAFKA_COMMIT_SECONDS_INTERVAL') or 10,
    'KAFKA_COMMIT_MESSAGES_INTERVAL': os.environ.get('KAFKA_COMMIT_MESSAGES_INTERVAL') or 10,
}

if docker:
    Configs.update({
        'POSTGRES_ADDRESS': os.environ.get('POSTGRES_ADDRESS') or 'postgres',
        'KAFKA_PORT': os.environ.get('KAFKA_PORT') or 9093,
        'KAFKA_ADDRESS': os.environ.get('KAFKA_SERVERS') or 'kafka',
        'ZOOKEEPER_ADDRESS': os.environ.get('ZOOKEEPER_HOST') or 'zookeeper',
        'REDIS_ADDRESS': os.environ.get('REDIS_HOST') or 'redis',
        'CASSANDRA_ADDRESS': os.environ.get('CASSANDRA_HOST') or 'cassandra',
    })

