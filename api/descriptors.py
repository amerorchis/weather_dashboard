def describe_pressure(pressure_hpa):
    """Convert pressure into barometer-type description."""
    pressure_hpa = float(pressure_hpa)
    if pressure_hpa < 970:
        description = "Storm"
    elif 970 <= pressure_hpa < 990:
        description = "Rain"
    elif 990 <= pressure_hpa < 1010:
        description = "Change"
    elif 1010 <= pressure_hpa < 1030:
        description = "Fair"
    elif pressure_hpa >= 1030:
        description = "Dry"
    else:
        description = ""
    return description


def describe_humidity(corrected_humidity):
    """Convert relative humidity into good/bad description."""
    corrected_humidity = float(corrected_humidity)
    if 40 < corrected_humidity < 60:
        return "Fair"
    elif corrected_humidity <= 40:
        return "Dry"
    else:
        return "Humid"

def describe_aqi(aqi):
    if aqi < 50:
        return "Good"
    elif 50 <= aqi < 100:
        return "Moderate"
    elif 100 <= aqi < 150:
        return "Unhealthy for Sensitive Groups"
    elif 150 <= aqi < 200:
        return "Unhealthy"
    elif 200 <= aqi < 300:
        return "Very Unhealthy"
    elif 300 <= aqi:
        return "Hazardous"
    