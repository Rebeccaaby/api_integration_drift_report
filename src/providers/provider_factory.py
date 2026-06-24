from src.providers.weatherapi_provider import WeatherApiProvider
from src.providers.meteostat_provider import MeteostatProvider
from src.providers.baseprovider import WeatherProvider

# When we want a provider, we add here to list
PROVIDER_LIST = {
    "weatherapi": WeatherApiProvider,
    "meteostat":  MeteostatProvider,
}

def get_provider(name: str, api_key: str) -> WeatherProvider:
    # Returns provider by config name, else an error
    if name not in PROVIDER_LIST:
        available = list(PROVIDER_LIST.keys())
        raise ValueError(f"Unknown provider: {name!r}. Available: {available}")

    provider_class = PROVIDER_LIST[name]
    return provider_class(api_key=api_key)
