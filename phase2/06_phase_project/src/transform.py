import pandas as pd
from api import ApiClient


def forecast_daily_to_df(apiobject: ApiClient) -> pd.DataFrame:
    return pd.DataFrame(apiobject.forecast_daily_list())
def forecast_hourly_to_df(apiobject: ApiClient) -> pd.DataFrame:
    return pd.DataFrame(apiobject.forecast_hourly_list())
def forecast_annually_to_df(apiobject: ApiClient) -> pd.DataFrame:
    return pd.DataFrame(apiobject.forecast_annually_daily_list())

def forecasted_hottest_days(apiobject):
    return forecast_daily_to_df(apiobject).sort_values('temperature_2m_max', ascending=False).loc[:10,['time', 'temperature_2m_max', 'city']].reset_index()
def hottest_days_year(apiobject):
    return forecast_annually_to_df(apiobject).sort_values('temperature_2m_max', ascending=False).loc[:11,['time', 'temperature_2m_max', 'city']].reset_index()
def rainiest_days_year(apiobject):
    return forecast_annually_to_df(apiobject).sort_values('rain_sum', ascending=False).loc[:11,['time', 'rain_sum', 'city']].reset_index()

def rain_days_year(apiobject):
    df = forecast_annually_to_df(apiobject)
    mask_rain = df['rain_sum'] > 0
    df['did_rain'] = mask_rain
    rain_days = df.groupby(['city'], as_index=False).agg(percentage = ('did_rain', 'mean')).sort_values(by='percentage', ascending= False)
    rain_days['percentage'] = (rain_days['percentage']*100).round(1)
    rain_days['year'] = apiobject.year
    rain_days = rain_days[['year', 'city', 'percentage']]
    return rain_days

def weekly_forecast_hours(apiobject, city):
    df = forecast_hourly_to_df(apiobject) 
    mask_city = df['city'] == city
    df_city = df[mask_city].copy()
    df_city['datetime'] = pd.to_datetime(df_city['time'])
    df_city = df_city.set_index('datetime')
    print('---------------------------------')
    print(f'Hourly forecast for {city}:')
    print('---------------------------------')
    return df_city[['temperature_2m', 'precipitation_probability']]

def weekly_forecast_days(apiobject, city):
    df = forecast_daily_to_df(apiobject)
    mask_city = df['city'] == city
    df_city = df[mask_city].copy()
    df_city['date'] = pd.to_datetime(df_city['time'])
    df_city = df_city.set_index('date')
    print('---------------------------------')
    print(f'Weekly forecast for {city}:')
    print('---------------------------------')
    return df_city[['temperature_2m_max', 'temperature_2m_min', 'precipitation_probability_max']]