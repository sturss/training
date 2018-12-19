import asyncio

from aiokafka import AIOKafkaConsumer, TopicPartition
from api.config import Configs
from api.logger import logger
from api.forms import MovieForm


if Configs['DATA_STORAGE'] == 'POSTGRES':
    from api.api_routes.services.postgres_data import insert_movie
else:
    from api.api_routes.services.cassandra_data import insert_movie


if Configs['OFFSET_STORAGE'] == 'ZOOKEEPER':
    from api.api_routes.services.zookeeper import ZookeeperManager as OffsetStorage
else:
    from api.api_routes.services.redis import RedisManager as OffsetStorage


class Consumer:
    consumer: AIOKafkaConsumer = None

    @classmethod
    async def read_messages(cls):
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
        while True:
            cls.consumer.commit()
            await asyncio.sleep(10)

    @classmethod
    async def _listen(cls):
        await cls._init()
        while True:
            try:
                message = await cls.consumer.getone()

                OffsetStorage.set_value('offset', OffsetStorage.get_value('offset')+1)

                counter = (OffsetStorage.get_value('offset_counter')+1) % 11
                OffsetStorage.set_value('offset_counter', counter)

                if counter == 10:
                    cls.consumer.commit()
                    logger.info("Consumer received 10th message, commit has been performed")

                cls.consumer.seek(TopicPartition(message.topic, message.partition), message.offset+1)

                data, errors = MovieForm().loads(message.value)
                if errors:
                    logger.error("Consumer received message with incorrect format %s", data)
                else:
                    await insert_movie(data)
            except Exception as e:
                logger.critical("Unexpected error, wait for 2sec: %s", e)
                if not cls.consumer:
                    await cls._init()
                await asyncio.sleep(2)

    @classmethod
    async def stop(cls):
        await cls.consumer.stop()
