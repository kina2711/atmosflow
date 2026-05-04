import psycopg2
from psycopg2.extras import execute_values
from loguru import logger
import time

class WeatherDBClient:
    def __init__(self, config):
        self.config = config
        self.conn = None
        self.connect()

    def connect(self):
        for i in range(5):
            try:
                self.conn = psycopg2.connect(
                    user=self.config.DB_USER, password=self.config.DB_PASS,
                    dbname=self.config.DB_NAME, host=self.config.DB_HOST, port=self.config.DB_PORT
                )
                self.conn.autocommit = True
                logger.info("Connected to Postgres!")
                return
            except Exception as e:
                logger.warning(f"DB Attempt {i+1} failed: {e}. Retrying...")
                time.sleep(5)
        raise Exception("Could not connect to DB")

    def insert_batch(self, data_list):
        query = "INSERT INTO raw_weather (city, temperature, humidity, description, event_time) VALUES %s"
        try:
            with self.conn.cursor() as cur:
                execute_values(cur, query, data_list)
            logger.info(f"Inserted {len(data_list)} records")
        except Exception as e:
            logger.error(f"Insert error: {e}")
            self.connect()