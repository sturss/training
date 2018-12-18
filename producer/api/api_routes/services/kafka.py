from kafka import KafkaProducer

producer = KafkaProducer(retries=5)


class Producer:
    pass