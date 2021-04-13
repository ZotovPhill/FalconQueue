import os

import requests

import celery


CELERY_BROKER = os.environ.get('CELERY_BROKER')
CELERY_BACKEND = os.environ.get('CELERY_BACKEND')

app = celery.Celery('tasks', broker=CELERY_BROKER, backend=CELERY_BACKEND)


@app.task
def find_out_weather(position: str):

    url = "https://community-open-weather-map.p.rapidapi.com/weather"

    querystring = {"q": position, "lang": "en", "units": "\"metric\"", "mode": "JSON"}

    headers = {
        'x-rapidapi-key': "",
        'x-rapidapi-host': "community-open-weather-map.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    return response.json()
