import pytest
from unittest.mock import patch
from ingestion.ingest_weather import fetch_weather_data

# Fake data to return
fake_weather_response = {
    "location": {
        "name": "San Francisco",
        "region": "California",
        "country": "United States of America",
        "lat": 37.78,
        "lon": -122.42,
        "tz_id": "America/Los_Angeles",
        "localtime_epoch": 1619641256,
        "localtime": "2021-04-28 15:07",
    },
    "current": {
        "last_updated_epoch": 1619640300,
        "last_updated": "2021-04-28 15:05",
        "temp_c": 18.0,
        "temp_f": 64.4,
        "is_day": 1,
        "condition": {
            "text": "Sunny",
            "icon": "//cdn.weatherapi.com/weather/64x64/day/113.png",
            "code": 1000,
        },
        "wind_mph": 6.9,
        "wind_kph": 11.2,
        "humidity": 71,
        "cloud": 0,
        "feelslike_c": 18.0,
        "feelslike_f": 64.4,
        "uv": 6.0,
    },
}


# Helper: MockResponse class
class MockResponse:
    def __init__(self, json_data, status_code=200):
        self._json_data = json_data
        self.status_code = status_code

    def json(self):
        return self._json_data

    def raise_for_status(self):
        if not (200 <= self.status_code < 300):
            raise Exception(f"HTTP {self.status_code} Error")


@patch("ingestion.ingest_weather.requests.get")
def test_fetch_weather_data_success(mock_get):
    mock_get.return_value = MockResponse(fake_weather_response)

    data = fetch_weather_data("San Francisco")

    assert isinstance(data, dict)
    assert "location" in data
    assert "current" in data
    assert data["location"]["name"] == "San Francisco"
    assert data["current"]["condition"]["text"] == "Sunny"


@patch("ingestion.ingest_weather.requests.get")
def test_fetch_weather_data_server_error(mock_get):
    # Mock the search API call to return 500 error
    mock_get.return_value = MockResponse({}, status_code=500)

    with pytest.raises(Exception) as exc_info:
        fetch_weather_data("San Francisco")

    assert "500" in str(exc_info.value)


@patch("ingestion.ingest_weather.requests.get")
def test_fetch_weather_data_empty_response(mock_get):
    # Mock an empty response
    mock_get.return_value = MockResponse({})

    with pytest.raises(ValueError) as exc_info:
        fetch_weather_data("NonexistentCity")

    assert "No data found for city" in str(exc_info.value)
