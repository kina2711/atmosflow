import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    KAFKA_BROKER = os.getenv("KAFKA_BROKER", "kafka:29092")
    KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "weather_data")
    KAFKA_GROUP_ID = "atmosflow-consumer-group"
    
    DB_USER = os.getenv("POSTGRES_USER")
    DB_PASS = os.getenv("POSTGRES_PASSWORD")
    DB_NAME = os.getenv("POSTGRES_DB")
    DB_HOST = os.getenv("DB_HOST", "postgres")
    DB_PORT = os.getenv("DB_PORT", "5432")
    
    BATCH_SIZE = 1