import time
from kafka import KafkaProducer

producer = None
while True:
    try:
        producer = KafkaProducer(retries=5, bootstrap_servers=['kafka:9092'])
        break
    except Exception as e:
        print(e)
        time.sleep(5)
