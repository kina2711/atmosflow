import requests
from datetime import datetime
from loguru import logger

class WeatherAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.openweathermap.org/data/2.5/weather"

    def get_weather(self, city):
        try:
            params = {"q": city, "appid": self.api_key, "units": "metric", "lang": "en"}
            response = requests.get(self.base_url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            return {
                "city": data["name"],
                "temp": data["main"]["temp"],
                "humidity": data["main"]["humidity"],
                "description": data["weather"][0]["description"],
                "event_time": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Error fetching {city}: {e}")
            return None