import logging

from sanic import Sanic

logger = logging.getLogger(__name__)

app = Sanic(__name__)

from api.api_routes import bp
app.blueprint(bp)
