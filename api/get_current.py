from convert import *
from descriptors import *
from query import query
import datetime

def get_current() -> tuple:
    # Grab last 2 minutes, if no data grab last 24 hours
    df = query('2 minutes')
    if len(df) == 0:
        df = query()

    # Find most recent reading
    recent = df['local_time'].max()
    current = df.loc[df['local_time'] == recent]

    # Retrieve each data point from most recent reading
    temp_F = str(round(convert_temp(current['Temp'].iloc[0])))
    humidity = str(round(float(current['Humidity'].iloc[0])))
    hum_desc = describe_humidity(humidity)
    pressure = str(round(float(current['Pressure'].iloc[0])))
    press_desc = describe_pressure(pressure)
    aqi = get_aqi(current['Particulates2_5'].iloc[0])
    aqi_desc = describe_aqi(aqi)
    _time = recent.strftime('%B %d, %-I:%M %p')

    return (temp_F, humidity, hum_desc, pressure, press_desc, aqi, aqi_desc, _time)

def get_dailies():
    # Calculate number of seconds elapsed today
    now = datetime.datetime.now()
    start_of_day = datetime.datetime(now.year, now.month, now.day)
    elapsed_seconds = (now - start_of_day).total_seconds()

    # Query records from today based on that
    df = query(f'{elapsed_seconds} seconds')

    # Identify and convert min and max temps
    low = df['Temp'].min()
    high = df['Temp'].max()
    low_F = str(round(convert_temp(float(low))))
    high_F = str(round(convert_temp(float(high))))
    return low_F, high_F
