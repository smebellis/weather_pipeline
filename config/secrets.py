import os
from dotenv import load_dotenv

load_dotenv()

WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

if WEATHER_API_KEY is None:
    raise Exception("Missing WEATHER_API_KEY. Please set it in your .env file.")
