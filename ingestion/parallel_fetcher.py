from concurrent.futures import ThreadPoolExecutor, as_completed
import time
from ingestion.ingest_weather import fetch_weather_data
from logger import get_logger

logger = get_logger("__name__")


def parallel_fetch_weather(cities, max_workers=5, requests_per_second=5):
    """
    Fetch weather data for multiple cities in parallel, respecting rate limits.

    Args:
        cities (list): List of city names.
        max_workers (int): Number of parallel threads.
        requests_per_second (int): Max allowed requests per second by API.

    Returns:
        dict: Mapping of city -> weather data
    """
    weather_results = {}
    batch_size = requests_per_second

    for i in range(0, len(cities), batch_size):
        batch = cities[i : i + batch_size]

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_city = {
                executor.submit(fetch_weather_data, city): city for city in batch
            }

            for future in as_completed(future_to_city):
                city = future_to_city[future]
                try:
                    data = future.result()
                    weather_results[city] = data
                    logger.info(f"Successfully fetched weather for {city}")
                except Exception as e:
                    logger.error(f"Failed to fetch weather for {city}: {e}")

        # Respect the rate limit
        if i + batch_size < len(cities):
            logger.info(f"Sleeping to respect rate limit...")
            time.sleep(1)  # Sleep 1 second between batches

    return weather_results
