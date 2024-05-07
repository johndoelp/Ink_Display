import requests
from train_secrets import secrets
from datetime import datetime

def train_call():
    # MBTA API URL
    url = "https://api-v3.mbta.com/predictions?filter[stop]=70064"

    # make API request
    headers = {"x-api-key": secrets['train_api']}
    response = requests.get(url, headers=headers)
    upcoming_trains = []
    if response.status_code == 200:
        schedule = response.json()
        # extract and print the estimated departure times of the next 1-2 trains, as predictions only delivers 1-2 upcoming trains data
        # if there are no current trains predicted (API call returns 200 but null), return False to trigger a 60s refresh in main.py
        try:
            if len(schedule) > 1:
                for i in range(len(schedule)):
                    if schedule["data"][i]["attributes"]["departure_time"] != None:
                        train_departure = datetime.strptime(schedule["data"][i]["attributes"]["departure_time"],"%Y-%m-%dT%H:%M:%S%z")
                        upcoming_trains.append(train_departure)
            else:
                train_departure = datetime.strptime(schedule["data"][0]["attributes"]["departure_time"],"%Y-%m-%dT%H:%M:%S%z")
                upcoming_trains.append(train_departure)
            return upcoming_trains
        except:
            print("Failed to retrieve train data.")
            return False
    else:
        print("Failed to retrieve train data.")
# print(train_call())