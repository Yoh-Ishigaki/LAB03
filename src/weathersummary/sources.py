import requests

from .config import SOURCE_URL, TIMEOUT
from .models import WeatherRecord


class WeatherSource:
    """Download Open-Meteo data and convert valid observations to records."""

    def __init__(self, url=SOURCE_URL, timeout=TIMEOUT):
        """Initialize the source with a URL and request timeout."""
        self.url = url
        self.timeout = timeout

    def download(self):
        """Download and return the decoded JSON response."""
        try:
            response = requests.get(self.url, timeout=self.timeout)
            response.raise_for_status()
            return response.json()
        except (requests.RequestException, ValueError) as exc:
            print(f"Download failed: {exc}")
            return None

    def fetch_records(self):
        """Download weather data and return validated WeatherRecord objects."""
        data = self.download()

        if data is None:
            return None

        if not isinstance(data, dict):
            print("Download failed: response was not a JSON object.")
            return None

        hourly = data.get("hourly")
        if not isinstance(hourly, dict):
            print("Download failed: hourly data is missing or malformed.")
            return None

        times = hourly.get("time")
        temperatures = hourly.get("temperature_2m")
        precipitation = hourly.get("precipitation")

        if not all(
            isinstance(value, list)
            for value in (times, temperatures, precipitation)
        ):
            print("Download failed: hourly fields are malformed.")
            return None

        records = []
        invalid_records = 0

        for time_value, temp_value, rain_value in zip(
            times, temperatures, precipitation
        ):
            try:
                records.append(
                    WeatherRecord(
                        time=time_value,
                        temperature=temp_value,
                        precipitation=rain_value,
                    )
                )
            except ValueError:
                invalid_records += 1

        if len(records) < 50:
            print(
                f"Download failed: only {len(records)} valid records were found; "
                "at least 50 are required."
            )
            return None

        # Keep the count available to the report without changing the record model.
        self.invalid_records = invalid_records
        return records
