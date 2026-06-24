import requests
from src.providers.baseprovider import WeatherProvider
from src.models.weatherInfo import WeatherInfo


class MeteostatProvider(WeatherProvider):
    # Meteostat returns metric units (C, mm, km/h
    BASE_URL = "https://meteostat.p.rapidapi.com/point/daily"
    HOST     = "meteostat.p.rapidapi.com"

    def get_weather(self, location_code: str, latitude: float, longitude: float, date: str) -> WeatherInfo:
        headers = {
            "x-rapidapi-key":  self.api_key,
            "x-rapidapi-host": self.HOST,
        }

        params = {
            "lat":   latitude,
            "lon":   longitude,
            "start": date,
            "end":   date,
        }

        response = requests.get(self.BASE_URL, headers=headers, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        info = data.get("data", [])
        if not info:
            raise ValueError(f"Meteostat returned no data for {location_code} on {date}")

        day = info[0]

        # Meteostat fields:
        # tavg=avg temp C, tmax=max temp C, tmin=min temp C
        # prcp=precipitation mm, wspd=wind speed km/h, rhum=relative humidity %

        avg_temp_f = self.celsius_to_fahrenheit(day["tavg"]) if day.get("tavg") is not None else None
        max_temp_f = self.celsius_to_fahrenheit(day["tmax"]) if day.get("tmax") is not None else None
        min_temp_f = self.celsius_to_fahrenheit(day["tmin"]) if day.get("tmin") is not None else None
        precip_in  = self.mm_to_inches(day["prcp"])          if day.get("prcp") is not None else None
        wind_mph   = self.kph_to_mph(day["wspd"])            if day.get("wspd") is not None else None
        humidity   = day.get("rhum")

        return WeatherInfo(
            source="meteostat",
            location=location_code,
            date=date,
            avg_temp_f=avg_temp_f,
            max_temp_f=max_temp_f,
            min_temp_f=min_temp_f,
            humidity=float(humidity) if humidity is not None else None,
            precipitation_in=precip_in,
            wind_mph=wind_mph,
        )
