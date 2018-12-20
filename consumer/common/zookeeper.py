"""
    Module with all functionality related to Redis
"""

from kazoo.client import KazooClient
from api.config import Configs
from api.logger import logger


class ZookeeperManager:
    logger.info("Establishing connection with Zookeeper: %s:%s", Configs['ZOOKEEPER_HOST'], Configs['ZOOKEEPER_PORT'])
    connection = KazooClient(hosts=f"{Configs['ZOOKEEPER_HOST']}:{Configs['ZOOKEEPER_PORT']}")
    connection.start()

    @classmethod
    def ensure_record(cls, node, value=0):
        if not cls.connection.exists(node):
            cls.connection.create(node)
            cls.connection.set(node, str(value).encode('utf-8'))
            logger.info("Zookeeper node %s didn't exist, node has been created", node)
        if not cls.connection.exists(f'{node}/data_type'):
            cls.connection.create(f'{node}/data_type')
            cls.connection.set(f'{node}/data_type', b'int')

    @classmethod
    def get_value(cls, node):
        cls.ensure_record(node)
        value = cls.connection.get(node)[0].decode('utf-8')
        data_type = cls.connection.get(f'{node}/data_type')[0].decode('utf-8')

        if data_type == 'int':
            value = int(value)
        elif data_type == 'float':
            value = float(value)

        return value

    @classmethod
    def set_value(cls, node, value):
        data_type = type(value).__name__
        cls.ensure_record(node)
        cls.connection.set(node, str(value).encode('utf-8'))
        cls.connection.set(f'{node}/data_type', str(data_type).encode('utf-8'))

    @classmethod
    def close(cls):
        cls.connection.close()
        logger.info('Closing connection with zookeeper')

    @classmethod
    def remove(cls, node):
        cls.connection.delete(node, recursive=True)

