import pytest
from unittest.mock import patch
from ingestion.parallel_fetcher import parallel_fetch_weather

# Fake data
fake_weather_response = {"location": {"name": "CityName"}, "current": {"temp_c": 20.0}}


class MockResponse:
    def __init__(self, json_data, status_code=200):
        self._json_data = json_data
        self.status_code = status_code

    def json(self):
        return self._json_data

    def raise_for_status(self):
        if not (200 <= self.status_code < 300):
            raise Exception(f"HTTP {self.status_code} Error")


@patch("ingestion.parallel_fetcher.fetch_weather_data")
def test_parallel_fetch_weather_success(mock_fetch_weather_data):
    cities = ["CityA", "CityB", "CityC"]

    # Setup: every city returns fake weather successfully
    mock_fetch_weather_data.side_effect = lambda city: {
        **fake_weather_response,
        "location": {"name": city},
    }

    results = parallel_fetch_weather(cities, max_workers=3, requests_per_second=3)

    assert isinstance(results, dict)
    assert len(results) == 3
    assert "CityA" in results
    assert results["CityA"]["location"]["name"] == "CityA"
