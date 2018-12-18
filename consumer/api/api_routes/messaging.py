from http import HTTPStatus

from sanic.request import Request
from sanic.response import json
from sanic.views import HTTPMethodView


class Message(HTTPMethodView):
    async def get(self, request : Request):
        return json({}, HTTPStatus.OK)
