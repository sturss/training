import datetime
import json
from http import HTTPStatus

from sanic.request import Request
from sanic.response import json, json_dumps
from sanic.views import HTTPMethodView

from .services.kafka import producer
from api.app import logger


class Message(HTTPMethodView):
    async def get(self, request: Request):
        message = {'title': 'New Movie 1',
                   'release_date': datetime.datetime.utcnow().isoformat()}
        producer.send('movies', message.encode('utf-8'))
        logger.critical("Message %s has been successfully sent to topic movies", message)
        return json({}, HTTPStatus.OK)
