from sanic import Sanic
from api.api_routes import bp

from api.api_routes.services.kafka import Consumer


app = Sanic(__name__)
app.blueprint(bp)

app.add_task(Consumer.read_messages())
