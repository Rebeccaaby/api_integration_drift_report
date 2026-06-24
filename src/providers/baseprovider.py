from abc import ABC, abstractmethod
from src.models.weatherInfo import WeatherInfo


class WeatherProvider(ABC):
    # Abstract base class for all weather providers

    def __init__(self, api_key: str):
        self.api_key = api_key

    @abstractmethod
    def get_weather(self, location_code: str, latitude: float, longitude: float, date: str) -> WeatherInfo:
        """Return WeatherInfo instance.
        Args:
            location_code : Airport code "DTW"
            latitude      : Location latitude
            longitude     : Location longitude
            date          : Date "2026-06-22"
        Returns:
            WeatherInfo with normalized fields
        """
        pass

    # shared unit conversion functions
    def celsius_to_fahrenheit(self, celsius: float) -> float:
        return round((celsius * 9 / 5) + 32, 2)

    def mm_to_inches(self, mm: float) -> float:
        return round(mm / 25.4, 4)

    def kph_to_mph(self, kph: float) -> float:
        return round(kph * 0.621371, 2)
