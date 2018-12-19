import asyncio

from aiokafka import AIOKafkaConsumer, TopicPartition
from api.config import Configs
from api.app import logger
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
            await Consumer.listen()
        finally:
            await Consumer.stop()

    @classmethod
    async def get_last_offset(cls):
        return TopicPartition('movie', 0), OffsetStorage.get_value('offset')

    @classmethod
    async def init(cls):
        OffsetStorage.ensure_record('offset', value=0)
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
                break
            except Exception as e:
                logger.critical(e)
                await asyncio.sleep(5)

        cls.consumer.seek(*await cls.get_last_offset())

    @classmethod
    async def listen(cls):
        await cls.init()
        while True:
            try:
                message = await cls.consumer.getone()
                cls.consumer.commit()
                OffsetStorage.set_value('offset', OffsetStorage.get_value('offset')+1)
                cls.consumer.seek(TopicPartition(message.topic, message.partition), message.offset+1)

                data, errors = MovieForm().loads(message.value)
                if errors:
                    raise ValueError(f"Wrong data format, {errors}")
                await insert_movie(data)
                await asyncio.sleep(0.1)
            except Exception as e:
                print(e)
                if not cls.consumer:
                    await cls.init()
                await asyncio.sleep(2)

    @classmethod
    async def stop(cls):
        await cls.consumer.stop()
