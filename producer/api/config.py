import os

docker = os.environ.get('DOCKER', None)


if not docker:
    Configs = {
        'KAFKA_SERVERS': os.environ.get('KAFKA_SERVERS') or 'localhost:9092',
    }
else:
    Configs = {
        'KAFKA_SERVERS': os.environ.get('KAFKA_SERVERS') or 'kafka:9092',
    }

