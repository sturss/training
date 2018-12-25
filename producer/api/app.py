"""
    Module with initializing Sanic application
"""
from sanic import Sanic

from api.api_routes import bp

app = Sanic(__name__)

app.blueprint(bp)
