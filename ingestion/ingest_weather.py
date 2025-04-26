import json
import requests
from logger import get_logger
from config.secrets import WEATHER_API_KEY
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

logger = get_logger("__name__")


def fetch_weather_data(city_name: str) -> dict:
    """
    Fetches weather data for the given city from the weather API.
    """

    search_url = (
        f"http://api.weatherapi.com/v1/current.json?key={WEATHER_API_KEY}&q={city_name}"
    )
    try:
        response = requests.get(search_url, timeout=10)
        response.raise_for_status()
    except requests.exceptions.HTTPError as errh:
        logger.error(f"Http Error: {errh}")
        raise Exception(f"Http Error occurred: {errh}")
    except requests.exceptions.ConnectionError as errc:
        logger.error(f"Connection Error: {errc}")
        raise Exception(f"Connection Error occurred: {errc}")
    except requests.exceptions.Timeout as errt:
        logger.error(f"Timeout Error {errt}")
        raise Exception(f"Timeout error occured {errt}")
    except requests.exceptions.RequestException as errr:
        logger.error(f"Something Else happened {errr}")
        raise Exception(f"Something Else happened {errr}")

    weather_data = response.json()
    if not weather_data:
        raise ValueError(f"No data found for city: {city_name}")

    logger.info(f"Successfully fetched weather data for {city_name}")
    return weather_data
