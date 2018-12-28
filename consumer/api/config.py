"""
    Module with application configurations
"""
import os

docker = os.environ.get('DOCKER', None)

Configs = {
    'POSTGRES_USER': os.environ.get('POSTGRES_USER') or 'admin',
    'POSTGRES_PASSWORD': os.environ.get('POSTGRES_PASSWORD') or 'admin',
    'POSTGRES_DATABASE': os.environ.get('POSTGRES_DATABASE') or 'movies',
    'POSTGRES_PORT': os.environ.get('POSTGRES_PORT') or 5432,
    'ZOOKEEPER_PORT': os.environ.get('ZOOKEEPER_PORT') or 2181,
    'REDIS_PORT': os.environ.get('REDIS_PORT') or 6379,
    'OFFSET_STORAGE': os.environ.get('OFFSET_STORAGE') or 'ZOOKEEPER',
    'DATA_STORAGE': os.environ.get('DATA_STORAGE') or 'CASSANDRA',
    'CASSANDRA_KEYSPACE': os.environ.get('CASSANDRA_KEYSPACE') or 'movies',
    'KAFKA_COMMIT_SECONDS_INTERVAL': os.environ.get('KAFKA_COMMIT_SECONDS_INTERVAL') or 10,
    'KAFKA_COMMIT_MESSAGES_INTERVAL': os.environ.get('KAFKA_COMMIT_MESSAGES_INTERVAL') or 10,
}

if not docker:
    Configs.update({
        'POSTGRES_ADDRESS': os.environ.get('POSTGRES_ADDRESS') or 'localhost',
        'KAFKA_ADDRESS': os.environ.get('KAFKA_SERVERS') or '0.0.0.0',
        'KAFKA_PORT': os.environ.get('KAFKA_PORT') or 9092,
        'ZOOKEEPER_HOST': os.environ.get('ZOOKEEPER_HOST') or 'localhost',
        'REDIS_HOST': os.environ.get('ZOOKEEPER_HOST') or 'localhost',
        'CASSANDRA_HOST': os.environ.get('CASSANDRA_HOST') or 'localhost',

    })
else:
    Configs.update({
        'POSTGRES_ADDRESS': os.environ.get('POSTGRES_ADDRESS') or 'postgres',
        'KAFKA_PORT': os.environ.get('KAFKA_PORT') or 9093,
        'KAFKA_ADDRESS': os.environ.get('KAFKA_SERVERS') or 'kafka',
        'ZOOKEEPER_HOST': os.environ.get('ZOOKEEPER_HOST') or 'zookeeper',
        'REDIS_HOST': os.environ.get('REDIS_HOST') or 'redis',
        'CASSANDRA_HOST': os.environ.get('CASSANDRA_HOST') or 'cassandra',
    })

