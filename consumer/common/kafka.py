"""
    Module with all functionality related to Kafka
"""

import asyncio
import time

from aiokafka import AIOKafkaConsumer, TopicPartition
from api.config import Configs
from api.logger import logger

if Configs['OFFSET_STORAGE'] == 'ZOOKEEPER':
    from common.zookeeper import ZookeeperManager as OffsetStorage
else:
    from common.redis import RedisManager as OffsetStorage


class Consumer:
    """
    Class for Consuming data from Kafka broker
    Works with topic movie
    Commits offset to Kafka every 10 seconds or on a new message
    """
    _consumer: AIOKafkaConsumer = None
    _reader_task: asyncio.Task = None
    _commit_task: asyncio.Task = None
    _uncommitted_messages = 0
    _listeners = set()
    _last_commit_time = None

    @classmethod
    def add_listener(cls, listener):
        cls._listeners.add(listener)

    @classmethod
    def remove_listener(cls, listener):
        cls._listeners.remove(listener)

    @classmethod
    async def connect(cls, on_message=()):
        if callable(on_message):
            cls._listeners.add(on_message)
        else:
            cls._listeners = cls._listeners.union(on_message)
        cls._reader_task = asyncio.ensure_future(cls._listen())

    @classmethod
    async def close(cls):
        try:
            cls._commit_task.cancel()
            cls._reader_task.cancel()
        except Exception as e:
            logger.error("Error occurred while trying to close connection with Kafka: %s", e)
        finally:
            if cls._consumer is not None:
                await cls._consumer.stop()

    @classmethod
    async def _get_last_offset(cls):
        return TopicPartition('movie', 0), await OffsetStorage.get_value('offset')

    @classmethod
    async def _init(cls):
        await OffsetStorage.ensure_record('offset', value=0)
        await OffsetStorage.ensure_record('offset_counter', value=0)

        cls._consumer = AIOKafkaConsumer('movie',
                                         group_id="movie_1",
                                         bootstrap_servers=f"{Configs['KAFKA_ADDRESS']}:{Configs['KAFKA_PORT']}",
                                         loop=asyncio.get_event_loop(),
                                         enable_auto_commit=False,
                                         consumer_timeout_ms=3000
                                         )
        while True:
            try:
                await cls._consumer.start()
                logger.info("Connection with Kafka broker successfully established")
                cls._commit_task = asyncio.ensure_future(cls._interval_commit())
                break
            except Exception as e:
                logger.error("Couldn't connect to Kafka broker because of %s, try again in 3 seconds", e)
                await asyncio.sleep(3)

        cls._consumer.seek(*await cls._get_last_offset())

    @classmethod
    async def _interval_commit(cls):
        if cls._last_commit_time is None:
            cls._last_commit_time = time.time()
        while True:
            passed_time = time.time() - cls._last_commit_time
            if passed_time < 10:
                await asyncio.sleep(10-passed_time)
                if time.time() - cls._last_commit_time < 10:
                    continue
            if cls._uncommitted_messages > 0:
                await cls._consumer.commit()
                logger.info("Planned interval commit")
                cls._uncommitted_messages = 0
            cls._last_commit_time = time.time()

    @classmethod
    async def _listen(cls):
        await cls._init()
        while True:
            try:
                message = await cls._consumer.getone()
                cls._uncommitted_messages += 1
                for listener in cls._listeners:
                    try:
                        listener(message)
                    except Exception as e:
                        logger.error("Error occurred in Consumer callback function: %s", e)

                await OffsetStorage.set_value('offset', await OffsetStorage.get_value('offset') + 1)

                counter = (await OffsetStorage.get_value('offset_counter') + 1) % 10
                await OffsetStorage.set_value('offset_counter', counter)

                if counter == 9:
                    await cls._consumer.commit()
                    cls._last_commit_time = time.time()
                    cls._uncommitted_messages = 0
                    logger.info("Consumer received 10th message, commit has been performed")

            except Exception as e:
                logger.critical("Unexpected error, wait for 2sec: %s", e)
                if not cls._consumer:
                    logger.critical("Connection with Kafka lost, try to reconnect")
                    await cls._init()
                await asyncio.sleep(2)
