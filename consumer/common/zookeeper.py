"""
    Module with all functionality related to Redis
"""

from kazoo.client import KazooClient
from api.config import Configs
from api.logger import logger


class ZookeeperManager:
    connection: KazooClient = None

    @classmethod
    def connect(cls):
        logger.info("Establishing connection with Zookeeper: %s:%s", Configs['ZOOKEEPER_HOST'],
                    Configs['ZOOKEEPER_PORT'])
        cls.connection = KazooClient(hosts=f"{Configs['ZOOKEEPER_HOST']}:{Configs['ZOOKEEPER_PORT']}")
        cls.connection.start()

    @classmethod
    def exists(cls, node):
        return cls.connection.exists(node)

    @classmethod
    def ensure_record(cls, node, value=0):
        if cls.exists(node):
            return

        cls.connection.create(node)
        cls.connection.create(f'{node}/data_type')
        logger.info("Zookeeper node %s didn't exist, node has been created", node)
        cls.set_value(node, value)

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
        if not cls.exists(node):
            cls.ensure_record(node, value)
        else:
            cls.connection.set(node, str(value).encode('utf-8'))
            cls.connection.set(f'{node}/data_type', str(data_type).encode('utf-8'))

    @classmethod
    def close(cls):
        logger.info('Closing connection with zookeeper')
        cls.connection.stop()
        cls.connection.close()

    @classmethod
    def remove(cls, node):
        cls.connection.delete(node, recursive=True)

