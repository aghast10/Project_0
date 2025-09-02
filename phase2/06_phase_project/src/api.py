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
        "daily": ["temperature_2m_max", "temperature_2m_min", "precipitation_probability_max"],
        "hourly": ["temperature_2m", "precipitation_probability"],
        "timezone": "Europe/Berlin",
        },
        timeout=1
        )
        return r.json()

    def forecast_daily_list(self):

        forecast_daily ={
            'time':[], 
            'temperature_2m_min':[], 
            'temperature_2m_max':[], 
            'precipitation_probability_max':[], 
            'city': []
        }

        for city in self.cities:
            forecast_raw = ApiClient.request_forecast_raw(self, city = city)
            for i, date in enumerate(forecast_raw['daily']['time']):
                forecast_daily['time'].append(date)
                forecast_daily['temperature_2m_min'].append(forecast_raw['daily']['temperature_2m_min'][i])
                forecast_daily['temperature_2m_max'].append(forecast_raw['daily']['temperature_2m_max'][i])
                forecast_daily['precipitation_probability_max'].append(forecast_raw['daily']['precipitation_probability_max'][i])
                forecast_daily['city'].append(city)

        return forecast_daily
    
    def forecast_hourly_list(self):

        forecast_hourly = {
            'time':[], 
            'temperature_2m':[], 
            'precipitation_probability':[], 
            'city': []
        }

        for city in self.cities:
            forecast_raw = ApiClient.request_forecast_raw(self, city = city)
            for i, date in enumerate(forecast_raw ['hourly']['time']):
                forecast_hourly['time'].append(date)
                forecast_hourly['temperature_2m'].append(forecast_raw['hourly']['temperature_2m'][i])
                forecast_hourly['precipitation_probability'].append(forecast_raw['hourly']['precipitation_probability'][i])
                forecast_hourly['city'].append(city)

        return forecast_hourly
    
    def forecast_annually_daily_raw(self, start_year:int, end_year:int, city:str) -> Dict[str, Any]:
        lat, lon = ApiClient.geocode(self, city)
        r = requests.get(
            URL_ARCHIVE,
            params = {
                "latitude": lat,
                "longitude": lon,
                "start_date": f"{start_year}-01-01",
                "end_date": f"{end_year}-12-31",
                "daily": ["temperature_2m_max", "temperature_2m_min", "precipitation_sum", "rain_sum"],
            },
            headers = {"Accept": "application/json"},
            timeout=1
        )
        return r.json()
        
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
            annually_forecast_raw: dict = ApiClient.forecast_annually_daily_raw(self, start_year=self.year, end_year=self.year, city=city)
            for i, date in enumerate(annually_forecast_raw['daily']['time']):
                annually_forecast['time'].append(date)
                annually_forecast['temperature_2m_min'].append(annually_forecast_raw['daily']['temperature_2m_min'][i])
                annually_forecast['temperature_2m_max'].append(annually_forecast_raw['daily']['temperature_2m_max'][i])
                annually_forecast['precipitation_sum'].append(annually_forecast_raw['daily']['precipitation_sum'][i])
                annually_forecast['rain_sum'].append(annually_forecast_raw['daily']['rain_sum'][i])
                annually_forecast['city'].append(city)
        
        return annually_forecast