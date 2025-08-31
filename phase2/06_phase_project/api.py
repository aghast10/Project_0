import requests

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

    def forecast_daily_list(self):

        forecast_daily ={'time':[], 'temperature_2m_min':[], 'temperature_2m_max':[], 'city': []}
        for city in self.cities:
            forecast_raw = ApiRequest.request_forecast_raw(self, c = city)
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
            forecast_raw = ApiRequest.request_forecast_raw(self, c = city)
            for i in forecast_raw ['hourly']['time']:
                forecast_hourly['time'].append(i)
            for i in forecast_raw['hourly']['temperature_2m']:
                forecast_hourly['temperature_2m'].append(i)
                forecast_hourly['city'].append(city)

        return forecast_hourly
    
    def forecast_annually_daily_list(self, year):
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