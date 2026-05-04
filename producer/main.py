import time
from config import Config
from weather_api import WeatherAPI
from kafka_client import WeatherKafkaProducer
from loguru import logger

def main():
    logger.info("Starting AtmosFlow Producer...")
    api = WeatherAPI(Config.API_KEY)
    kafka_prod = WeatherKafkaProducer(Config.KAFKA_BROKER)

    while True:
        for city in Config.CITIES:
            data = api.get_weather(city)
            if data: kafka_prod.send_data(Config.KAFKA_TOPIC, data)
            time.sleep(1)
        time.sleep(Config.FETCH_INTERVAL)

if __name__ == "__main__":
    main()