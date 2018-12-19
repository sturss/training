from http import HTTPStatus

from sanic.request import Request
from sanic.response import json
from sanic.views import HTTPMethodView

from api.api_routes.services.postgres_data import get_movies


class Message(HTTPMethodView):
    async def get(self, request : Request):
        return json({'count': await get_movies()}, HTTPStatus.OK)
