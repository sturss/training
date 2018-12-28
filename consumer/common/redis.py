"""
    Module with all functionality related to Redis
"""
import asyncio
import aioredis as rd

from api.config import Configs
from api.logger import logger

from common.connection import Connection


class RedisManager:
    """
        Class which encapsulates all necessary operations for working with Redis
        if provided methods are not sufficient, Redis.connection may be used
        for direct access
    """
    connection: rd.Redis = None

    @classmethod
    async def connect(cls):
        """
        Creates Redis object with given in configurations host and initiates connection
        :return: None
        """
        logger.info("Establishing connection with Redis: %s:%s", Configs['REDIS_ADDRESS'], Configs['REDIS_PORT'])
        for i in range(Configs['REDIS_CONNECTION_RETRIES']):
            try:
                cls.connection = await rd.create_redis(f"redis://{Configs['REDIS_ADDRESS']}:{Configs['REDIS_PORT']}",
                                                       loop=asyncio.get_event_loop())
                logger.info("Connection with Redis has been established successfully")
                break
            except Exception as e:
                logger.warning("Couldn't connect to Redis, another try in %s seconds: %s",
                               Configs['REDIS_CONNECTION_TIMEOUT'], e)
                await asyncio.sleep(Configs['REDIS_CONNECTION_TIMEOUT'])
        else:
            logger.critical("Couldn't connect to Redis, check your settings and try again."
                            " (Consider increasing number of retries)")

    @classmethod
    async def close(cls):
        """
        Closes connection with Redis if established and sets connection object to None
        :return: None
        """
        if cls.connection:
            logger.info("Closing connection with Redis: %s:%s", Configs['REDIS_HOST'], Configs['REDIS_PORT'])
            cls.connection.close()
            await cls.connection.wait_closed()
            cls.connection = None

    @classmethod
    @Connection.check_connection
    async def ensure_record(cls, key, value=0):
        """
        Checks if given node exists. If exists return, else creates node and sets value to 0 or a given
        :param key: str
        :param value: value to set the key
        :return: None
        """
        if not await cls.connection.exists(key):
            await cls.set_value(key, value)

    @classmethod
    @Connection.check_connection
    async def get_value(cls, key):
        """
        Returns value of the node with basic data types casting.
        :param key: str
        :return: str, int , or float - value placed in the given node
        """
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
        """
        Checks data type of a given value and stores both value and data type in a list
        :param key: str
        :param value: str or any other data type which will be casted to str
        :return: None
        """
        data_type = type(value).__name__
        if await cls.connection.exists(key):
            await cls.connection.delete(key)
        await cls.connection.lpush(key, value)
        await cls.connection.rpush(key, data_type)

