from config import Config
from db_client import WeatherDBClient
from kafka_consumer import WeatherKafkaConsumer
from loguru import logger

def main():
    logger.info("Starting AtmosFlow Consumer...")
    db = WeatherDBClient(Config)
    consumer = WeatherKafkaConsumer(Config.KAFKA_BROKER, Config.KAFKA_TOPIC, Config.KAFKA_GROUP_ID)
    batch = []
    try:
        for data in consumer.poll_messages():
            record = (data.get('city'), data.get('temp'), data.get('humidity'), data.get('description'), data.get('event_time'))
            batch.append(record)
            if len(batch) >= Config.BATCH_SIZE:
                db.insert_batch(batch)
                batch = []
    except Exception as e:
        logger.error(f"Critical error: {e}")

if __name__ == "__main__":
    main()