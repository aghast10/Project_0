import requests
import pandas as pd
import json
import sqlite3
from paths import FORECAST_DAILY_JSON, FORECAST_HOURLY_JSON, FORECAST_DATABASE


class ApiRequest:
    def __init__(self, cities):
        self.cities = cities
    
    def geocode(self, c):
        
        from paths import url1
        r1 = requests.get(
            url1, 
            params={"name": c, "language":'en'}, 
            headers = {"Accept": "application/json"},
            timeout=1
            )

        latitude = r1.json()['results'][0]['latitude']
        longitude = r1.json()['results'][0]['longitude']
        coordinates = [latitude, longitude]
        return coordinates
    
    def request_forecast_raw(self, c):
        coordinates = ApiRequest.geocode(self, c)
        from paths import url2
        r = requests.get(
        url2,
        params = {
        "latitude": coordinates[0],
        "longitude": coordinates[1],
        "daily": ["temperature_2m_max", "temperature_2m_min"],
        "hourly": "temperature_2m",
        "timezone": "Europe/Berlin",
        },
        headers = {"Accept": "application/json"},
        timeout=1
        )
        forecast_raw = r.json()
        return forecast_raw

    def forecast_daily_list(self, cities):

        forecast_daily ={'time':[], 'temperature_2m_min':[], 'temperature_2m_max':[], 'city': []}
        for city in cities:
            forecast_raw = ApiRequest.request_forecast_raw(self, c = city)
            for i in forecast_raw['daily']['time']:
                forecast_daily['time'].append(i)
            for i in forecast_raw['daily']['temperature_2m_min']:
                forecast_daily['temperature_2m_min'].append(i)
            for i in forecast_raw['daily']['temperature_2m_max']:
                forecast_daily['temperature_2m_max'].append(i)
                forecast_daily['city'].append(city)
        
        return forecast_daily
    
    def forecast_hourly_list(self, cities):
        forecast_hourly = {'time':[], 'temperature_2m':[], 'city': []}
        for city in cities:
            forecast_raw = ApiRequest.request_forecast_raw(self, c = city)
            for i in forecast_raw ['hourly']['time']:
                forecast_hourly['time'].append(i)
            for i in forecast_raw['hourly']['temperature_2m']:
                forecast_hourly['temperature_2m'].append(i)
                forecast_hourly['city'].append(city)

        return forecast_hourly
    
    def forecast_annually_daily_list(self, city, year):
        from paths import url3
        annually_forecast ={
                'time':[], 
                'temperature_2m_min':[], 
                'temperature_2m_max':[], 
                'precipitation_sum':[],
                'rain_sum':[],
                'city': []
        }

        for city in self.cities:
            coordinates = ApiRequest.geocode(self, city)
            r = requests.get(
                url3,
                params = {
                    "latitude": coordinates[0],
	                "longitude": coordinates[1],
                    "start_date": f"{year}-01-01",
                    "end_date": f"{year}-12-31",
                    "daily": ["temperature_2m_max", "temperature_2m_min", "precipitation_sum", "rain_sum"],
                },
            headers = {"Accept": "application/json"},
            timeout=1
            )
            annually_forecast_raw = r.json()
    
            for i in annually_forecast_raw['daily']['time']:
                annually_forecast['time'].append(i)
            for i in annually_forecast_raw['daily']['temperature_2m_min']:
                annually_forecast['temperature_2m_min'].append(i)
            for i in annually_forecast_raw['daily']['temperature_2m_max']:
                annually_forecast['temperature_2m_max'].append(i)
                annually_forecast['city'].append(city)
            for i in annually_forecast_raw['daily']['precipitation_sum']:
                annually_forecast['precipitation_sum'].append(i)
            for i in annually_forecast_raw['daily']['rain_sum']:
                annually_forecast['rain_sum'].append(i)
        
        return annually_forecast


if __name__ == '__main__':
    cities = ['MADRID', 'OVIEDO', 'ZARAGOZA', 'BARCELONA', 'VALENCIA', 'SEVILLA', 'BILBAO']
    example = ApiRequest(cities)

    with open(FORECAST_DAILY_JSON, "w", encoding="utf-8") as f:
        json.dump(example.forecast_daily_list(cities), f, indent=4)

    with open(FORECAST_HOURLY_JSON, "w", encoding="utf-8") as f:
        json.dump(example.forecast_hourly_list(cities), f, indent=4)

    forecast_daily_df = pd.read_json(FORECAST_DAILY_JSON)

    with sqlite3.connect(FORECAST_DATABASE) as conn:
        cur = conn.cursor()
        forecast_daily_df.to_sql('forecast_daily', conn, if_exists='replace')

    top_hottest_days = forecast_daily_df.sort_values('temperature_2m_max', ascending=False).iloc[:11,[0,2,3]].reset_index()
