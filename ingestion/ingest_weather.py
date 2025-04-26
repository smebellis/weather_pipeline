import json
import requests
from logger import get_logger

logger = get_logger("__name__")


def fetch_weather_data(city_name: str) -> json:
    """
    Fetches weather data for the given city from the MetaWeather API.
    """
    # Find the city's WOEID (Where on earth ID)
    search_url = f"https://www.metaweather.com/api/location/search/?query={city_name}"
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

    # Parse the WOEID from the search result
    search_result = response.json()
    if not search_result:
        raise ValueError(f"No Data found for city: {city_name}")
    woeid = search_result[0]["woeid"]

    # Fetch the weather using the WOEID
    weather_url = f"https://www.metaweather.com/api/location/{woeid}/"
    try:
        weather_response = requests.get(weather_url, timeout=10)
        weather_response.raise_for_status()
    except requests.exceptions.RequestException as err:
        logger.error(f"Failed Fetching weather data: {err}")
        raise Exception(f"Failed fetching weather data: {err}")

    logger.info(f"Successfully fetched weather data for {city_name}")
    return weather_response.json()
