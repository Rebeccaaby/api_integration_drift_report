import requests
from src.providers.baseprovider import WeatherProvider
from src.models.weatherInfo import WeatherInfo


class WeatherApiProvider(WeatherProvider):
    # WeatherAPI returns imperial units (F, mph, inches)
    BASE_URL = "http://api.weatherapi.com/v1/history.json"

    def get_weather(self, location_code: str, latitude: float, longitude: float, date: str) -> WeatherInfo:
        params = {
            "key": self.api_key,
            "q":   f"{latitude},{longitude}",
            "dt":  date,
        }

        response = requests.get(self.BASE_URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        #WeatherAPI response
        day = data["forecast"]["forecastday"][0]["day"]

        return WeatherInfo(
            source="weatherapi",
            location=location_code,
            date=date,
            avg_temp_f=round(day.get("avgtemp_f", 0), 2),
            max_temp_f=round(day.get("maxtemp_f", 0), 2),
            min_temp_f=round(day.get("mintemp_f", 0), 2),
            humidity=round(day.get("avghumidity", 0), 2),
            precipitation_in=round(day.get("totalprecip_in", 0), 4),
            wind_mph=round(day.get("maxwind_mph", 0), 2),
        )
