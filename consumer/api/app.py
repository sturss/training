import logging

from sanic import Sanic


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

from api.api_routes.services.kafka import Consumer
from api.api_routes import bp

app = Sanic(__name__)
app.add_task(Consumer.read_messages())

app.blueprint(bp)

