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
        # TODO: Handle errors later, what could be an error we see?
        # HTTPerror, ConnectionError, Timeout, RequestException
    except requests.exceptions.HTTPError as errh:
        # TODO: add logging statements instead of print
        logger.info(f"Http Error: {errh}")
        raise Exception(f"Http Error occurred: {errh}")
    except requests.exceptions.ConnectionError as errc:
        logger.info(f"Connection Error: {errc}")
        raise Exception(f"Connection Error occurred: {errc}")
    except requests.exceptions.Timeout as errt:
        print("Timeout Error", errt)
    except requests.exceptions.RequestException as errr:
        print("Something Else happened", errr)

    # Parse the WOEID from the search result
    search_result = response.json()
    if not search_result:
        raise ValueError(f"No Data found for city: {city_name}")
    woeid = search_result[0]["woeid"]

    # Fetch the weather using the WOEID
    weather_url = f"https://www.metaweather.com/api/location/{woeid}/"
    weather_response = requests.get(weather_url, timeout=10)
    weather_data = weather_response.json()

    return weather_data
