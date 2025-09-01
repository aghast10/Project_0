import requests
from typing import Tuple, Dict, Any
from paths import URL_GEOCODE, URL_FORECAST, URL_ARCHIVE

class ApiClient:
    """Open-Meteo Client(geocoding, 
    forecast, archive)."""
    def __init__(self, cities: list, year:int):
        self.cities = cities
        self.year = year
    def geocode(self, city:str) -> Tuple[float, float]:
        
        r1 = requests.get(
            URL_GEOCODE, 
            params={"name": city, "language":'en'}, 
            headers = {"Accept": "application/json"},
            timeout=1
            )

        lat = float(r1.json()['results'][0]['latitude'])
        lon = float(r1.json()['results'][0]['longitude'])
        
        return lat, lon #devuelve un tuple
    
    def request_forecast_raw(self, city:str) -> Dict[str, Any]:
        lat, lon = ApiClient.geocode(self, city) #creamos un tuple que da lo que devuelva geocode
        r = requests.get(
        URL_FORECAST,
        params = {
        "latitude": lat,
        "longitude": lon,
        "daily": ["temperature_2m_max", "temperature_2m_min"],
        "hourly": "temperature_2m",
        "timezone": "Europe/Berlin",
        },
        timeout=1
        )
        return r.json()

    def forecast_daily_list(self):

        forecast_daily ={'time':[], 'temperature_2m_min':[], 'temperature_2m_max':[], 'city': []}
        for city in self.cities:
            forecast_raw = ApiClient.request_forecast_raw(self, city = city)
            for i in forecast_raw['daily']['time']:
                forecast_daily['time'].append(i)
            for i in forecast_raw['daily']['temperature_2m_min']:
                forecast_daily['temperature_2m_min'].append(i)
            for i in forecast_raw['daily']['temperature_2m_max']:
                forecast_daily['temperature_2m_max'].append(i)
                forecast_daily['city'].append(city)
        
        return forecast_daily
    
    def forecast_hourly_list(self):
        forecast_hourly = {'time':[], 'temperature_2m':[], 'city': []}
        for city in self.cities:
            forecast_raw = ApiClient.request_forecast_raw(self, city = city)
            for i in forecast_raw ['hourly']['time']:
                forecast_hourly['time'].append(i)
            for i in forecast_raw['hourly']['temperature_2m']:
                forecast_hourly['temperature_2m'].append(i)
                forecast_hourly['city'].append(city)

        return forecast_hourly
    
    def forecast_annually_daily_list(self):
        annually_forecast ={
                'time':[], 
                'temperature_2m_min':[], 
                'temperature_2m_max':[], 
                'precipitation_sum':[],
                'rain_sum':[],
                'city': []
        }

        for city in self.cities:
            coordinates = ApiClient.geocode(self, city)
            r = requests.get(
                URL_ARCHIVE,
                params = {
                    "latitude": coordinates[0],
	                "longitude": coordinates[1],
                    "start_date": f"{self.year}-01-01",
                    "end_date": f"{self.year}-12-31",
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