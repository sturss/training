"""
    Module with application endpoints for /movies namespace
"""

import json
from http import HTTPStatus

from sanic.request import Request
from sanic.response import json, json_dumps
from sanic.views import HTTPMethodView

from api.api_routes.services.kafka import producer
from api.logger import logger


class Message(HTTPMethodView):
    async def post(self, request: Request):
        title = request.json.get('title')
        release_date = request.json.get('release_date')
        message = json_dumps({'title': title,
                              'release_date': release_date})
        producer.send('movie', message.encode('utf-8'))
        logger.info("Message %s has been successfully sent to topic movies", message)
        return json({}, HTTPStatus.OK)
