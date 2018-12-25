"""
    Module with all functionality related to Redis
"""
import asyncio
import aioredis as rd

from api.config import Configs
from api.logger import logger

from common.connection import Connection


class RedisManager:
    connection: rd.Redis = None

    @classmethod
    async def connect(cls):
        logger.info("Establishing connection with Redis: %s:%s", Configs['REDIS_HOST'], Configs['REDIS_PORT'])
        cls.connection = await rd.create_redis(f"redis://{Configs['REDIS_HOST']}:{Configs['REDIS_PORT']}",
                                               loop=asyncio.get_event_loop())

    @classmethod
    async def close(cls):
        if cls.connection:
            logger.info("Closing connection with Redis: %s:%s", Configs['REDIS_HOST'], Configs['REDIS_PORT'])
            cls.connection.close()
            await cls.connection.wait_closed()
            cls.connection = None

    @classmethod
    @Connection.check_connection
    async def ensure_record(cls, key, value=0):
        if not await cls.connection.exists(key):
            await cls.set_value(key, value)

    @classmethod
    @Connection.check_connection
    async def get_value(cls, key):
        await cls.ensure_record(key)
        value = (await cls.connection.lindex(key, 0)).decode('utf-8')
        data_type = (await cls.connection.lindex(key, 1)).decode('utf-8')

        if data_type == 'int':
            value = int(value)
        elif data_type == 'float':
            value = float(value)

        return value

    @classmethod
    @Connection.check_connection
    async def set_value(cls, key, value):
        data_type = type(value).__name__
        if await cls.connection.exists(key):
            await cls.connection.delete(key)
        await cls.connection.lpush(key, value)
        await cls.connection.rpush(key, data_type)

