import requests

# http://opendata.smhi.se/apidocs/metfcst/parameters.html
weather_code = {
    1: "Clear sky",
    2: "Nearly clear sky",
    3: "Variable cloudiness",
    4: "Halfclear sky",
    5: "Cloudy sky",
    6: "Overcast",
    7: "Fog",
    8: "Light rain showers",
    9: "Moderate rain showers",
    10: "Heavy rain showers",
    11: "Thunderstorm",
    12: "Light sleet showers",
    13: "Moderate sleet showers",
    14: "Heavy sleet showers",
    15: "Light snow showers",
    16: "Moderate snow showers",
    17: "Heavy snow showers",
    18: "Light rain",
    19: "Moderate rain",
    20: "Heavy rain",
    21: "Thunder",
    22: "Light sleet",
    23: "Moderate sleet",
    24: "Heavy sleet",
    25: "Light snowfall",
    26: "Moderate snowfall",
    27: "Heavy snowfall",
}

def forecast_url(category, version, longitude, latitude):
    return f"https://opendata-download-metfcst.smhi.se/api/category/{category}/version/{version}/geotype/point/lon/{longitude}/lat/{latitude}/data.json"

def forecast_request(category, version, longitude, latitude):
    return requests.get(forecast_url(category, version, longitude, latitude)).json()

def forecast_json(long, lat):
    return forecast_request("pmp3g", "2", long, lat)

def forecast_timestamps(long, lat):
    data = forecast_json(long, lat)
    timestamps = []
    for series in data['timeSeries']:
        stamp = series['validTime']
        weather_index = next(filter(lambda param: param['name'] == 'Wsymb2', series['parameters']))
        weather = weather_code[weather_index['values'][0]]
        timestamps.append((stamp, weather))
    
    return timestamps

