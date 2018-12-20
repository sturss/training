"""
    Module with initializing Sanic application
"""
from sanic import Sanic

from api.api_routes.services.kafka import Consumer
from api.api_routes import bp

app = Sanic(__name__)
app.add_task(Consumer.read_messages())  # Makes Consumer start reading messages after creating application object

app.blueprint(bp)

