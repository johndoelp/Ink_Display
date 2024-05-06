import requests
from train_secrets import secrets
from datetime import datetime

def train_call():
    # MBTA API URL
    url = "https://api-v3.mbta.com/predictions?filter[stop]=70064"

    # Set up the headers with API key
    headers = {
        "x-api-key": secrets['train_api']
    }

    # Make the API request
    response = requests.get(url, headers=headers)
    upcoming_trains = []
    if response.status_code == 200:
        schedule = response.json()
        # Extract and print the estimated departure times of the next two trains
        if len(schedule) > 1:
            for i in range(len(schedule)):
                if schedule["data"][i]["attributes"]["departure_time"] != None:
                    train_departure = datetime.strptime(schedule["data"][i]["attributes"]["departure_time"],"%Y-%m-%dT%H:%M:%S%z")
                    upcoming_trains.append(train_departure)
        else:
            train_departure = datetime.strptime(schedule["data"][0]["attributes"]["departure_time"],"%Y-%m-%dT%H:%M:%S%z")
            upcoming_trains.append(train_departure)
        return upcoming_trains

    else:
        print("Failed to retrieve train data.")
print(train_call())