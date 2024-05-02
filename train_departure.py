#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import json
import requests
import csv

def train_call():
    upcoming_trains = []
    # MBTA API key
    api_key = "0aea58a21bcc40e9b16679f428d7e99e"

    # Construct the API URL
    #url = "https://api-v3.mbta.com/predictions?filter[stop]={70064}&filter[direction_id]=0&sort=departure_time&include=stop,trip"
    url = "https://api-v3.mbta.com/predictions?filter%5Bstop%5D=70064"

    # Set up the headers with API key
    headers = {
        "x-api-key": api_key
    }

    # Make the API request
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        predictions = data.get("data", [])

        # Extract and print the arrival times of the next two trains
        for i, prediction in enumerate(predictions[:4]):
            departure_time = prediction["attributes"]["departure_time"]
            t = departure_time.index("T")
            upcoming_trains.append(departure_time[11:19])
        print(upcoming_trains)
        return upcoming_trains

    else:
        print(f"Failed to retrieve data. Status code: {response.status_code}")

train_call()