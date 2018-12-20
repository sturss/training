"""
    Module with application endpoints for /movies namespace
"""

from http import HTTPStatus

from sanic.request import Request
from sanic.response import json
from sanic.views import HTTPMethodView

from api.api_routes.services.postgres_data import get_movies


class Message(HTTPMethodView):
    from api.api_routes.services.kafka_callbacks import movie_call_back
    from common.kafka import Consumer

    Consumer.add_listener(movie_call_back)

    async def get(self, request : Request):
        return json({'count': await get_movies()}, HTTPStatus.OK)
