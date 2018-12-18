from kafka import KafkaProducer

producer = KafkaProducer(retries=5, bootstrap_servers=['kafka:9092'])
