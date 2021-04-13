import json

import falcon
from celery.result import AsyncResult
from falcon import Request, Response

from tasks import find_out_weather


class HelloWorldResource:
    def on_get(self, request, response):
        response.media = (
            """
            Hello World from Falcon Python with
            Gunicorn running in an Alpine Linux container.
            """
        )


class OpenMapWeatherResource:
    def on_post(self, request: Request, response: Response):
        raw_json = request.stream.read()
        request_data = json.loads(raw_json, encoding='utf-8')
        location = str(request_data['location'])
        task = find_out_weather.delay(location)
        response.status = falcon.HTTP_201
        result = {
            "status": "CREATED",
            "data": {
                "task_id": task.id
            }
        }
        response.body = json.dumps(result)


class CheckWeatherResult:
    def on_get(self, request: Request, response: Response, task_id: str):
        task_result = AsyncResult(task_id)
        weather_data = task_result.result
        response.status = falcon.HTTP_200
        result = {
            "name": weather_data['name'],
            "temperature": weather_data['main'],
            "wind": weather_data['wind']
        }
        response.body = json.dumps(result)
