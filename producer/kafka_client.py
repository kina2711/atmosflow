import json
from kafka import KafkaProducer
from loguru import logger
import time

class WeatherKafkaProducer:
    def __init__(self, broker):
        self.broker = broker
        self.producer = self._connect()

    def _connect(self):
        for attempt in range(1, 6):
            try:
                logger.info(f"Attempt {attempt}/5: Connecting to Kafka at {self.broker}...")
                producer = KafkaProducer(
                    bootstrap_servers=[self.broker],
                    value_serializer=lambda v: json.dumps(v).encode('utf-8')
                )
                logger.info("Connected to Kafka successfully!")
                return producer
            except Exception as e:
                logger.warning(f"Kafka connection attempt {attempt} failed: {e}")
                if attempt < 5:
                    time.sleep(5)
                else:
                    logger.error("Max retries reached. Kafka is unavailable.")
                    raise e

    def send_data(self, topic, data):
        try:
            self.producer.send(topic, value=data)
            self.producer.flush()
            logger.info(f"Sent {data['city']} to Kafka")
        except Exception as e:
            logger.error(f"Error sending to Kafka: {e}")