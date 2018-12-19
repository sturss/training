import datetime
import json
from http import HTTPStatus

from sanic.request import Request
from sanic.response import json, json_dumps
from sanic.views import HTTPMethodView

from api.api_routes.services.kafka import producer
from api.logger import logger


class Message(HTTPMethodView):
    async def get(self, request: Request):
        message = json_dumps({'title': 'New Movie 1',
                              'release_date': datetime.datetime.utcnow().isoformat()})
        try:
            producer.send('movie', message.encode('utf-8'))
        except Exception as e:
            logger.critical(e)
        logger.critical("Message %s has been successfully sent to topic movies", message)
        return json({}, HTTPStatus.OK)
