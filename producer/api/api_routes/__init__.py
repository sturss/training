"""
    Module where all blueprints for namespaces are created
"""

from sanic import Blueprint

from api.api_routes.movies import (
    Message
)

bp = Blueprint(name='movies', url_prefix='/movies')

bp.add_route(Message.as_view(), '/')





