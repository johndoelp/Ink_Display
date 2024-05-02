#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import time
import json
from sys import exit

import requests

# query OpenMetero for current weather & forecast for Boston
def get_weather():

    weather_url = "https://api.open-meteo.com/v1/gfs?latitude=42.3876&longitude=-71.0995&current=temperature_2m,is_day,weather_code&daily=weather_code,temperature_2m_max,temperature_2m_min,sunrise,sunset,precipitation_probability_max&temperature_unit=fahrenheit&wind_speed_unit=mph&precipitation_unit=inch&timezone=America%2FNew_York"

    weather = {}
    res = requests.get(weather_url)
    if res.status_code == 200:
        j = json.loads(res.text)

        daily = j["daily"]
        weather["dates"] = daily["time"]
        weather["forecasted_weather_codes"] = daily["weather_code"]
        weather["forecasted_temp_maxes"] = daily["temperature_2m_max"]
        weather["forecasted_temp_mins"] = daily["temperature_2m_min"]
        weather["forecasted_sunrises"] = daily["sunrise"]
        weather["forecasted_sunsets"] = daily["sunset"]
        weather["forecasted_precip_chances"] = daily["precipitation_probability_max"]

        return weather
    else:
        return weather



def forecast_parser():
    # create dictionary for weather forecast
    forecasted_weather_days = []
    weather_icon = None
    current_weather_icon = None
    weather = get_weather()

    # map icons to weather_code
    icon_map = {
        "snow": [71, 73, 75, 77, 85, 86],
        "rain": [51, 53, 55, 56, 57, 61, 63, 65, 66, 67, 80, 81, 82],
        "cloud": [1, 2, 3, 45, 48],
        "sun": [0],
        "storm": [95, 96, 99],
        "wind": []
    }

    for i in range(1,5):
        forecasted_weather_day = {
            "date": weather["dates"][i],
            "weather_icon": weather["forecasted_weather_codes"][i],
            "temp_max": weather["forecasted_temp_maxes"][i],
            "temp_min": weather["forecasted_temp_mins"][i],
            "sunrise": weather["forecasted_sunrises"][i],
            "sunset": weather["forecasted_sunsets"][i],
            "precipitation_chance": weather["forecasted_precip_chances"][i],
        }
        for icon in icon_map:
            if weather["forecasted_weather_codes"][i] in icon_map[icon]:
                weather_icon = icon
                break
        forecasted_weather_day.update({"weather_icon": weather_icon})
        forecasted_weather_days.append(forecasted_weather_day)

    return forecasted_weather_days