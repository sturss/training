"""
    Module with all functionality related to Redis
"""

import redis as rd

from api.config import Configs
from api.logger import logger


class RedisManager:
    logger.info("Establishing connection with Redis: %s:%s", Configs['REDIS_HOST'], Configs['REDIS_PORT'])
    connection = rd.StrictRedis(host=Configs['REDIS_HOST'], port=Configs['REDIS_PORT'])

    @classmethod
    def ensure_record(cls, key, value=0):
        if not cls.connection.exists(key):
            cls.set_value(key, value)

    @classmethod
    def get_value(cls, key):
        cls.ensure_record(key)
        value = cls.connection.lindex(key, 0).decode('utf-8')
        data_type = cls.connection.lindex(key, 1).decode('utf-8')

        if data_type == 'int':
            value = int(value)
        elif data_type == 'float':
            value = float(value)

        return value

    @classmethod
    def set_value(cls, key, value):
        data_type = type(value).__name__
        if cls.connection.exists(key):
            cls.connection.delete(key)
        cls.connection.lpush(key, value)
        cls.connection.rpush(key, data_type)

