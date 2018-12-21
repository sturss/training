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
    consumer: AIOKafkaConsumer = None
    listeners = set()
    last_commit_time = None

    @classmethod
    def add_listener(cls, listener):
        cls.listeners.add(listener)

    @classmethod
    def remove_listener(cls, listener):
        cls.listeners.remove(listener)

    @classmethod
    async def read_messages(cls, on_message=()):
        if callable(on_message):
            cls.listeners.add(on_message)
        else:
            cls.listeners.union(on_message)
        try:
            await Consumer._listen()
        finally:
            await Consumer.stop()

    @classmethod
    async def _get_message_counter(cls):
        return OffsetStorage.get_value('offset_counter')

    @classmethod
    async def _get_last_offset(cls):
        return TopicPartition('movie', 0), OffsetStorage.get_value('offset')

    @classmethod
    async def _init(cls):
        OffsetStorage.ensure_record('offset', value=0)
        OffsetStorage.ensure_record('offset_counter', value=0)
        loop = asyncio.get_event_loop()
        cls.consumer = AIOKafkaConsumer('movie',
                                        group_id="movie_1",
                                        bootstrap_servers=Configs['KAFKA_SERVERS'],
                                        loop=loop,
                                        auto_offset_reset='earliest',
                                        enable_auto_commit=False,
                                        consumer_timeout_ms=3000
                                        )
        while True:
            try:
                await cls.consumer.start()
                logger.info("Connection with Kafka broker successfully established")
                asyncio.ensure_future(cls._interval_commit())
                break
            except Exception as e:
                logger.error("Couldn't connect to Kafka broker because of %s, try again in 5sec", e)
                await asyncio.sleep(5)

        cls.consumer.seek(*await cls._get_last_offset())

    @classmethod
    async def _interval_commit(cls):
        if cls.last_commit_time is None:
            cls.last_commit_time = time.time()
        while True:
            passed_time = time.time() - cls.last_commit_time
            if passed_time < 10:
                await asyncio.sleep(10-passed_time)
                if time.time() - cls.last_commit_time < 10:
                    continue
            await cls.consumer.commit()
            cls.last_commit_time = time.time()
            logger.critical("COMMIT")

    @classmethod
    async def _listen(cls):
        await cls._init()
        while True:
            try:
                message = await cls.consumer.getone()

                for listener in cls.listeners:
                    try:
                        listener(message)
                    except Exception as e:
                        logger.error("Error occurred in Consumer callback function: %s", e)

                OffsetStorage.set_value('offset', OffsetStorage.get_value('offset') + 1)

                counter = (OffsetStorage.get_value('offset_counter') + 1) % 10
                OffsetStorage.set_value('offset_counter', counter)

                if counter == 9:
                    await cls.consumer.commit()
                    cls.last_commit_time = time.time()
                    logger.info("Consumer received 10th message, commit has been performed")

                cls.consumer.seek(TopicPartition(message.topic, message.partition), message.offset + 1)

            except Exception as e:
                logger.critical("Unexpected error, wait for 2sec: %s", e)
                if not cls.consumer:
                    await cls._init()
                await asyncio.sleep(2)

    @classmethod
    async def stop(cls):
        await cls.consumer.stop()
