import pandas as pd

def forecast_daily_to_df(apiobject):
    return pd.DataFrame(apiobject.forecast_daily_list())
def forecast_hourly_to_df(apiobject):
    return pd.DataFrame(apiobject.forecast_hourly_list())
def forecast_annually_to_df(apiobject):
    return pd.DataFrame(apiobject.forecast_annually_daily_list())

def forecasted_hottest_days(apiobject):
    return forecast_daily_to_df(apiobject).sort_values('temperature_2m_max', ascending=False).iloc[:11,[0,2,3]].reset_index()
def hottest_days_year(apiobject):
    return forecast_annually_to_df(apiobject).sort_values('temperature_2m_max', ascending=False).iloc[:11,[0,2,5]].reset_index()
def rainiest_days_year(apiobject):
    return forecast_annually_to_df(apiobject).sort_values('rain_sum', ascending=False).iloc[:11,[0,4,5]].reset_index()

def rain_days_year(apiobject):
    df = forecast_annually_to_df(apiobject)
    mask_rain = df['rain_sum'] > 0
    df['did_rain'] = mask_rain
    rain_days = df.groupby(['city'], as_index=False).agg(percentage = ('did_rain', 'mean')).sort_values(by='percentage', ascending= False)
    rain_days['percentage'] = (rain_days['percentage']*100).round(1)
    rain_days['year'] = apiobject.year
    rain_days = rain_days[['year', 'city', 'percentage']]
    return rain_days
