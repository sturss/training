"""
    Module with all functionality related to Kafka
"""
import time
from kafka import KafkaProducer

from api.logger import logger
from api.config import Configs

producer = None
while True:
    try:
        producer = KafkaProducer(retries=1, bootstrap_servers=Configs['KAFKA_SERVERS'])
        break
    except Exception as e:
        logger.error("Couldn't connect, try in 5 seconds: ", e)
        time.sleep(5)
