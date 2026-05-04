import json
from kafka import KafkaConsumer
from loguru import logger

class WeatherKafkaConsumer:
    def __init__(self, broker, topic, group_id):
        self.consumer = KafkaConsumer(
            topic, bootstrap_servers=[broker],
            group_id=group_id, auto_offset_reset='earliest',
            value_deserializer=lambda x: json.loads(x.decode('utf-8'))
        )
        logger.info("Connected to Kafka Topic!")

    def poll_messages(self):
        for message in self.consumer:
            yield message.value