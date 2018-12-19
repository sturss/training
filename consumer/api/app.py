
from sanic import Sanic

from api.api_routes.services.kafka import Consumer
from api.api_routes import bp

app = Sanic(__name__)
app.add_task(Consumer.read_messages())

app.blueprint(bp)

