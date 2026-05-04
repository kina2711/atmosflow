import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    KAFKA_BROKER = os.getenv("KAFKA_BROKER", "kafka:29092")
    KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "weather_data")
    CITIES = ["Ho Chi Minh", "Hanoi", "Hue", "Can Tho"]
    FETCH_INTERVAL = 60
    API_KEY = os.getenv("WEATHER_API_KEY")