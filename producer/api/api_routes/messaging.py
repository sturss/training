import datetime
import json
from http import HTTPStatus

from sanic.request import Request
from sanic.response import json, json_dumps
from sanic.views import HTTPMethodView

from api.api_routes.services.kafka import producer


class Message(HTTPMethodView):
    async def get(self, request: Request):
        date = datetime.datetime.utcnow().isoformat()
        print(str(date))
        producer.send('movies', json_dumps({'title': 'Movie 1',
                                            'release_date': date}).encode('utf-8'))
        return json({}, HTTPStatus.OK)
