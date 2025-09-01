import json
import sqlite3
import requests_cache
from datetime import datetime
import pandas as pd
from api import ApiClient
import paths

requests_cache.install_cache("cache", expire_after= 3600)

cities = ['MADRID', 'OVIEDO', 'ZARAGOZA', 'BARCELONA', 'VALENCIA', 'SEVILLA', 'BILBAO']
year = 2024
default_cities = ApiClient(cities)

forecast_daily_df = pd.DataFrame(default_cities.forecast_daily_list())
forecast_hourly_df = pd.DataFrame(default_cities.forecast_hourly_list())
forecast_annually_df = pd.DataFrame(default_cities.forecast_annually_daily_list(year))

forecasted_hottest_days = forecast_daily_df.sort_values('temperature_2m_max', ascending=False).iloc[:11,[0,2,3]].reset_index()

hottest_days_2024 = forecast_annually_df.sort_values('temperature_2m_max', ascending=False).iloc[:11,[0,2,5]].reset_index()
rainiest_days_2024 = forecast_annually_df.sort_values('rain_sum', ascending=False).iloc[:11,[0,4,5]].reset_index()


mask_rain = forecast_annually_df['rain_sum'] > 0
forecast_annually_df['did_rain'] = mask_rain
rain_days_2024 = forecast_annually_df.groupby(['city'], as_index=False).agg(percentage = ('did_rain', 'mean')).sort_values(by='percentage', ascending= False)
rain_days_2024['percentage'] = (rain_days_2024['percentage']*100).round(1)
rain_days_2024['year'] = year
rain_days_2024 = rain_days_2024[['year', 'city', 'percentage']]

# --------------
# EXPORTS TO CSV
# --------------
now_tag = datetime.now().strftime('%d%m%Y')
rainiest_days_2024.to_csv(paths.EXPORT_DIR/f"rainiest_days_{year}.csv", index=False)
rain_days_2024.to_csv(paths.EXPORT_DIR/f"rain_days_{year}.csv", index=False)
hottest_days_2024.to_csv(paths.EXPORT_DIR/f"hottest_days_{year}.csv", index=False)
forecasted_hottest_days.to_csv(paths.EXPORT_DIR/f"forecasted_hottest_days{now_tag}.csv", index=False)

# --------------
# EXPORTS TO SQL
# --------------
with sqlite3.connect(paths.FORECAST_DATABASE) as conn:
    cur = conn.cursor()
    forecast_daily_df.to_sql('forecast_daily', conn, if_exists='replace')
    forecast_hourly_df.to_sql('forecast_hourly', conn, if_exists='replace')
    forecast_annually_df.to_sql('2024_weather', conn, if_exists='replace')


print(forecast_annually_df)
print(hottest_days_2024)
print(rainiest_days_2024)
print(rain_days_2024)