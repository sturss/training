"""
    Module with application configurations
"""

import os

docker = os.environ.get('DOCKER', None)


if not docker:
    Configs = {
        'KAFKA_ADDRESS': os.environ.get('KAFKA_ADDRESS') or 'localhost',
        'KAFKA_PORT': os.environ.get('KAFKA_PORT') or 9092,
    }
else:
    Configs = {
        'KAFKA_ADDRESS': os.environ.get('KAFKA_ADDRESS') or 'kafka',
        'KAFKA_PORT': os.environ.get('KAFKA_PORT') or 9092,
    }

