import requests
from train_secrets import secrets
from datetime import datetime

def train_call():
    upcoming_trains = []

    # MBTA API URL
    url = "https://api-v3.mbta.com/schedules?filter[stop]=70064"

    # Set up the headers with API key
    headers = {
        "x-api-key": secrets['train_api']
    }

    # Make the API request
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        predictions = data.get("data", [])

        # Extract and print the departure times of the next four trains
        for i, prediction in enumerate(predictions[:4]):
            departure_time = prediction["attributes"]["departure_time"]
            if datetime.strptime(departure_time,"%Y-%m-%dT%H:%M:%SZ") > datetime.now("-04:00"):
                upcoming_trains.append(departure_time[11:19])
        print(upcoming_trains)
        return upcoming_trains

    else:
        print(f"Failed to retrieve data. Status code: {response.status_code}")
train_call()