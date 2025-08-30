import json
import sqlite3
import requests_cache
from datetime import datetime
import pandas as pd
from api import ApiRequest
from paths import FORECAST_DAILY_JSON, FORECAST_HOURLY_JSON, FORECAST_DATABASE, EXPORT_DIR, FORECAST_ANNUALLY_DAILY_JSON

requests_cache.install_cache("cache", expire_after= 3600)

cities = ['MADRID', 'OVIEDO', 'ZARAGOZA', 'BARCELONA', 'VALENCIA', 'SEVILLA', 'BILBAO']
spain_cities = ApiRequest(cities)

with open(FORECAST_DAILY_JSON, "w", encoding="utf-8") as f:
    json.dump(spain_cities.forecast_daily_list(cities), f, indent=4)

with open(FORECAST_HOURLY_JSON, "w", encoding="utf-8") as f:
    json.dump(spain_cities.forecast_hourly_list(cities), f, indent=4)

with open(FORECAST_ANNUALLY_DAILY_JSON, "w", encoding="utf-8") as f:
    json.dump(spain_cities.forecast_annually_daily_list(cities, 2024), f, indent=4)

forecast_daily_df = pd.read_json(FORECAST_DAILY_JSON)
forecast_hourly_df = pd.read_json(FORECAST_HOURLY_JSON)
forecast_annually_df = pd.read_json(FORECAST_ANNUALLY_DAILY_JSON)

with sqlite3.connect(FORECAST_DATABASE) as conn:
    cur = conn.cursor()
    forecast_daily_df.to_sql('forecast_daily', conn, if_exists='replace')
    forecast_hourly_df.to_sql('forecast_hourly', conn, if_exists='replace')

now_tag = datetime.now().strftime('%d%m%Y')
forecasted_hottest_days = forecast_daily_df.sort_values('temperature_2m_max', ascending=False).iloc[:11,[0,2,3]].reset_index()
forecasted_hottest_days.to_csv(EXPORT_DIR/f"forecasted_hottest_days{now_tag}.csv", index=False)
    