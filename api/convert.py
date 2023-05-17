import aqi

def convert_temp(c) -> float:
    c = float(c)
    temp = (c * (9 / 5)) + 32
    return temp

def get_aqi(pm25):
    return int(aqi.to_iaqi(aqi.POLLUTANT_PM25, pm25, algo=aqi.ALGO_EPA))
