"""
    Module with all functionality related to Kafka
"""
import time
from kafka import KafkaProducer

from api.logger import logger

producer = None
while True:
    try:
        producer = KafkaProducer(retries=1, bootstrap_servers=['kafka:9092'])
        break
    except Exception as e:
        logger.error(e)
        time.sleep(5)
