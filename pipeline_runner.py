from ingestion.parallel_fetcher import parallel_fetch_weather

# from storage.save_raw import save_raw_data
from logger import get_logger

import datetime

logger = get_logger("PipelineRunner")


def main():
    try:
        logger.info("Pipeline started.")

        # 1. Define your list of cities
        cities = ["San Francisco", "New York", "Chicago", "Los Angeles", "Austin"]

        # 2. Fetch all weather data in parallel
        weather_data = parallel_fetch_weather(
            cities, max_workers=5, requests_per_second=5
        )

        # 3. Save raw data
        # timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        # save_raw_data(weather_data, f"weather_raw_{timestamp}.json")

        logger.info("Pipeline completed successfully.")

    except Exception as e:
        logger.error(f"Pipeline failed: {e}")
        # Optional: alert or send notification here


if __name__ == "__main__":
    main()
