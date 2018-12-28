"""
    Module with all functionality related to Zookeeper
"""
import asyncio
from aiozk import ZKClient
from api.config import Configs
from api.logger import logger

from common.connection import Connection


class ZookeeperManager:
    """
        Class which encapsulates all necessary operations for working with Zookeeper
        if provided methods are not sufficient, ZookeeperManager.connection may be used
        for direct access
    """
    connection: ZKClient = None

    @classmethod
    async def connect(cls):
        """
        Creates ZKClient object with given in configurations host and initiates connection
        :return: None
        """
        logger.info("Establishing connection with Zookeeper: %s:%s", Configs['ZOOKEEPER_ADDRESS'],
                    Configs['ZOOKEEPER_PORT'])
        cls.connection = ZKClient(f"{Configs['ZOOKEEPER_ADDRESS']}:{Configs['ZOOKEEPER_PORT']}")
        for i in range(Configs['ZOOKEEPER_CONNECTION_RETRIES']):
            try:
                await cls.connection.start()
                logger.info("Connection with Zookeeper has been established successfully")
                break
            except Exception as e:
                logger.warning("Couldn't connect to Zookeeper, another try in %s seconds: %s",
                               Configs['ZOOKEEPER_CONNECTION_TIMEOUT'], e)
                await asyncio.sleep(Configs['ZOOKEEPER_CONNECTION_TIMEOUT'])
        else:
            logger.critical("Couldn't connect to Zookeeper, check your settings and try again."
                            " (Consider increasing number of retries)")

    @classmethod
    async def close(cls):
        """
        Closes connection with Zookeeper if established and sets connection object to None
        :return: None
        """
        if cls.connection:
            logger.info('Closing connection with zookeeper')
            await cls.connection.close()
            cls.connection = None

    @classmethod
    @Connection.check_connection
    async def exists(cls, node):
        """
        Returns whether given node exists or not
        :param node: str - name of node
        :return: Bool
        """
        return await cls.connection.exists(node)

    @classmethod
    @Connection.check_connection
    async def ensure_record(cls, node, value=0):
        """
        Checks if given node exists. If exists return, else creates node and sets value to 0 or a given
        :param node: str - name of node
        :param value: value to set the node
        :return: None
        """
        if await cls.exists(node):
            return

        await cls.connection.create(node)
        await cls.connection.create(f'{node}/data_type')
        logger.info("Zookeeper node %s didn't exist, node has been created", node)
        await cls.set_value(node, value)

    @classmethod
    @Connection.check_connection
    async def get_value(cls, node):
        """
        Returns value of the node with basic data types casting.
        :param node: str - name of node
        :return: str, int , or float - value placed in the given node
        """
        await cls.ensure_record(node)
        value = (await cls.connection.get_data(node)).decode('utf-8')
        data_type = (await cls.connection.get_data(f'{node}/data_type')).decode('utf-8')

        if data_type == 'int':
            value = int(value)
        elif data_type == 'float':
            value = float(value)

        return value

    @classmethod
    @Connection.check_connection
    async def set_value(cls, node, value):
        """
        Checks data type of a given value and stores both value and data type according to the following pattern
            value - /path/to/node/
            data type - /path/to/node/data_type
        :param node: str - name of node
        :param value: str or any other data type which will be casted to str
        :return: None
        """
        data_type = type(value).__name__
        if not await cls.exists(node):
            await cls.ensure_record(node, value)
        else:
            await cls.connection.set_data(node, str(value).encode('utf-8'))
            await cls.connection.set_data(f'{node}/data_type', str(data_type).encode('utf-8'))

    @classmethod
    @Connection.check_connection
    async def remove(cls, node):
        """
        Removes node and all children nodes recursively
        :param node: str - name of node
        :return: None
        """
        await cls.connection.deleteall(node)

