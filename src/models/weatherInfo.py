from dataclasses import dataclass
from typing import Optional


@dataclass
class WeatherInfo:
    # Normalized weather data model.
    source:           str            # weatherapi
    location:         str            # location
    date:             str           

    avg_temp_f:       Optional[float] = None   # since weather apis don't always return every field
    max_temp_f:       Optional[float] = None   
    min_temp_f:       Optional[float] = None
    humidity:         Optional[float] = None   # Meteostat doesn't return humidity in free tier
    precipitation_in: Optional[float] = None
    wind_mph:         Optional[float] = None

    def to_dict(self) -> dict:
        # dictionary format for JSON/CSV file
        return {
            "source":           self.source,
            "location":         self.location,
            "date":             self.date,
            "avg_temp_f":       self.avg_temp_f,
            "max_temp_f":       self.max_temp_f,
            "min_temp_f":       self.min_temp_f,
            "humidity":         self.humidity,
            "precipitation_in": self.precipitation_in,
            "wind_mph":         self.wind_mph,
        }

    def __repr__(self):
        return (
            f"WeatherInfo(source={self.source!r}, location={self.location!r}, "
            f"date={self.date!r}, avg_temp_f={self.avg_temp_f}, "
            f"max_temp_f={self.max_temp_f}, min_temp_f={self.min_temp_f}, "
            f"humidity={self.humidity}, precipitation_in={self.precipitation_in}, "
            f"wind_mph={self.wind_mph})"
        )
