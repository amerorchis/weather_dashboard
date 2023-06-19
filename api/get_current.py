from api.convert import *
from api.descriptors import *
from api.query import query
from datetime import datetime, timedelta
import pytz

def get_current() -> tuple:
    # Grab last 2 minutes, if no data grab last 24 hours
    df = query('2 minutes')
    if len(df) == 0:
        df = query()

    # Find most recent reading
    recent = df['local_time'].max()
    current = df.loc[df['local_time'] == recent]
    
    if not current.empty:
        # Retrieve each data point from most recent reading
        temp_F = str(round(convert_temp(current['Temp'].iloc[0])))
        humidity = str(round(float(current['Humidity'].iloc[0])))
        hum_desc = describe_humidity(humidity)
        pressure = str(round(float(current['Pressure'].iloc[0])))
        press_desc = describe_pressure(pressure)
        aqi = get_aqi(current['Particulates2_5'].iloc[0])
        aqi_desc = describe_aqi(aqi)
        _time = recent.strftime('%B %-d, %-I:%M %p')

        return (temp_F, humidity, hum_desc, pressure, press_desc, aqi, aqi_desc, _time)
    
    else:
        return False, False, False, False, False, False, False, False

def get_dailies():
    # Find now and start of day in MT
    mt = pytz.timezone('America/Denver')  # Replace 'YOUR_TIMEZONE' with your desired time zone
    now_mt = datetime.now(pytz.utc).astimezone(mt)
    start_of_day = datetime(now_mt.year, now_mt.month, now_mt.day, tzinfo=mt)

    # Calculate the elapsed seconds since the start of the day
    elapsed_seconds = (now_mt - start_of_day).total_seconds()

    # Query records from today based on that
    df = query(f'{elapsed_seconds} seconds')

    if not df.empty:

        # Identify and convert min and max temps
        low = df['Temp'].min()
        high = df['Temp'].max()
        low_F = str(round(convert_temp(float(low))))
        high_F = str(round(convert_temp(float(high))))
        return low_F, high_F

    else:
        return False, False
    