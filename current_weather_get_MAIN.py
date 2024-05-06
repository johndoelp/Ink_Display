
import datetime
import json

import requests

# query OpenMetero for current weather & forecast for weather_url
def get_weather():
    weather_url = "https://api.open-meteo.com/v1/gfs?latitude=42.3876&longitude=-71.0995&current=temperature_2m,is_day,weather_code&daily=weather_code,temperature_2m_max,temperature_2m_min,sunrise,sunset,precipitation_probability_max&temperature_unit=fahrenheit&wind_speed_unit=mph&precipitation_unit=inch&timezone=America%2FNew_York"
    weather = {}
    res = requests.get(weather_url)
    if res.status_code == 200:
        j = json.loads(res.text)
        current = j["current"]
        weather["now_temperature"] = current["temperature_2m"]
        weather["now_is_day"] = current["is_day"]
        weather["now_weather_code"] = current["weather_code"]

        daily = j["daily"]
        weather["forecasted_temp_maxes"] = daily["temperature_2m_max"]
        weather["forecasted_temp_mins"] = daily["temperature_2m_min"]
        weather["forecasted_sunrises"] = daily["sunrise"]
        weather["forecasted_sunsets"] = daily["sunset"]
        weather["forecasted_precip_chances"] = daily["precipitation_probability_max"]
        return weather
    else:
        return weather

def current_parser():
    weather = get_weather()

    # create dictionary for current conditions
    weather_icon = None
    current_weather = []

    # weather_icon name match
    # map icons to weather_code
    icon_map = {
        "snow": [71, 73, 75, 77, 85, 86],
        "rain": [51, 53, 55, 56, 57, 61, 63, 65, 66, 67, 80, 81, 82],
        "cloud": [1, 2, 3, 45, 48],
        "sun": [0],
        "storm": [95, 96, 99],
        "wind": []
    }

    current_conditions = {
        "current temperature": weather["now_temperature"],
        "current daytime": weather["now_is_day"],
        "current weather icon": weather["now_weather_code"],
        "temp_max": weather["forecasted_temp_maxes"][0],
        "temp_min": weather["forecasted_temp_mins"][0],
        "sunrise": datetime.datetime.strptime(weather["forecasted_sunrises"][0],'%Y-%m-%dT%H:%M'),
        "sunset": datetime.datetime.strptime(weather["forecasted_sunsets"][0],'%Y-%m-%dT%H:%M'),
        "precipitation_chance": weather["forecasted_precip_chances"][0]
    }
    for icon in icon_map:
        if current_conditions["current weather icon"] in icon_map[icon]:
            weather_icon = icon
            break
    current_conditions.update({"current weather icon": weather_icon})
    current_weather.append(current_conditions)

    # print(current_weather)
    return current_weather