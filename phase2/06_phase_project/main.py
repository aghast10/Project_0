from datetime import datetime
import requests_cache
from api import ApiClient
from transform import (
    rainiest_days_year, 
    rain_days_year,
    hottest_days_year,
    forecasted_hottest_days,
    forecast_annually_to_df
)
from db import pipeline
from paths import EXPORT_DIR
requests_cache.install_cache("cache", expire_after= 3600)

def main():
    cities = ['MADRID', 'OVIEDO', 'ZARAGOZA', 'BARCELONA', 'VALENCIA', 'SEVILLA', 'BILBAO']
    year = 2024

    apiobject = ApiClient(cities, year)

    # --------------
    # EXPORTS TO CSV
    # --------------
    now_tag = datetime.now().strftime('%d%m%Y')
    rainiest_days_year(apiobject).to_csv(EXPORT_DIR/f"rainiest_days_{year}.csv", index=False)
    rain_days_year(apiobject).to_csv(EXPORT_DIR/f"rain_days_{year}.csv", index=False)
    hottest_days_year(apiobject).to_csv(EXPORT_DIR/f"hottest_days_{year}.csv", index=False)
    forecasted_hottest_days(apiobject).to_csv(EXPORT_DIR/f"forecasted_hottest_days{now_tag}.csv", index=False)

    # --------------
    # EXPORTS TO SQL
    # --------------
    pipeline(apiobject)

    # --------------
    # PRINTS
    # --------------
    print(forecast_annually_to_df(apiobject))
    print(hottest_days_year(apiobject))
    print(rainiest_days_year(apiobject))
    print(rain_days_year(apiobject))

if __name__ == "__main__":
    main()