from pathlib import Path

BASE_DIR = Path('phase2/06_phase_project')
EXPORT_DIR = BASE_DIR/"exports"
EXPORT_DIR.mkdir(parents=True, exist_ok=True)

FORECAST_DAILY_JSON = EXPORT_DIR/'forecast_daily.json'
FORECAST_HOURLY_JSON = EXPORT_DIR/'forecast_hourly.json'
FORECAST_DATABASE = EXPORT_DIR/'forecast.db'
FORECAST_ANNUALLY_DAILY_JSON = EXPORT_DIR/'forecast_annually.json'

URL_GEOCODE = 'https://geocoding-api.open-meteo.com/v1/search'
URL_FORECAST = 'https://api.open-meteo.com/v1/forecast'
URL_ARCHIVE = 'https://archive-api.open-meteo.com/v1/archive'
