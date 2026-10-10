from pathlib import Path

SOURCE_URL = (
    "https://api.open-meteo.com/v1/forecast"
    "?latitude=43.65&longitude=79.38"
    "&hourly=temperature_2m,precipitation"
    "&past_days=7&forecast_days=0"
    "&timezone=America/Toronto"
)

TIMEOUT = 10

PROJECT_ROOT = Path(__file__).resolve().parents[2]
OUTPUT_PATH = PROJECT_ROOT / "data" / "processed" / "summary.json"
