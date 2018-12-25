"""
    Module with all functionality related to Redis
"""

from aiozk import ZKClient
from api.config import Configs
from api.logger import logger


class ZookeeperManager:
    connection: ZKClient = None

    @classmethod
    async def connect(cls):
        logger.info("Establishing connection with Zookeeper: %s:%s", Configs['ZOOKEEPER_HOST'],
                    Configs['ZOOKEEPER_PORT'])
        cls.connection = ZKClient(f"{Configs['ZOOKEEPER_HOST']}:{Configs['ZOOKEEPER_PORT']}")
        await cls.connection.start()

    @classmethod
    async def exists(cls, node):
        return await cls.connection.exists(node)

    @classmethod
    async def ensure_record(cls, node, value=0):
        if await cls.exists(node):
            return

        await cls.connection.create(node)
        await cls.connection.create(f'{node}/data_type')
        logger.info("Zookeeper node %s didn't exist, node has been created", node)
        await cls.set_value(node, value)

    @classmethod
    async def get_value(cls, node):
        await cls.ensure_record(node)
        value = (await cls.connection.get_data(node)).decode('utf-8')
        data_type = (await cls.connection.get_data(f'{node}/data_type')).decode('utf-8')

        if data_type == 'int':
            value = int(value)
        elif data_type == 'float':
            value = float(value)

        return value

    @classmethod
    async def set_value(cls, node, value):
        data_type = type(value).__name__
        if not await cls.exists(node):
            await cls.ensure_record(node, value)
        else:
            await cls.connection.set_data(node, str(value).encode('utf-8'))
            await cls.connection.set_data(f'{node}/data_type', str(data_type).encode('utf-8'))

    @classmethod
    async def close(cls):
        logger.info('Closing connection with zookeeper')
        await cls.connection.close()

    @classmethod
    async def remove(cls, node):
        await cls.connection.delete(node)

