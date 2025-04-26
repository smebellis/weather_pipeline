import pytest
from unittest.mock import patch
from ingestion.ingest_weather import fetch_weather_data

# Fake data to return
fake_search_response = [{"woeid": 2487956}]
fake_weather_response = {"consolidated_weather": [{"weather_state_name": "Clear"}]}


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
    # Mock two API calls in sequence
    mock_get.side_effect = [
        MockResponse(fake_search_response),
        MockResponse(fake_weather_response),
    ]

    data = fetch_weather_data("San Francisco")

    assert isinstance(data, dict)
    assert "consolidated_weather" in data
    assert data["consolidated_weather"][0]["weather_state_name"] == "Clear"


@patch("ingestion.ingest_weather.requests.get")
def test_fetch_weather_data_server_error(mock_get):
    # Mock the search API call to return 500 error
    mock_get.return_value = MockResponse(fake_search_response, status_code=500)

    with pytest.raises(Exception) as exc_info:
        fetch_weather_data("San Francisco")

    assert "HTTP 500" in str(exc_info.value)
