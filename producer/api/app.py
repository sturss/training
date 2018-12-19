from sanic import Sanic

app = Sanic(__name__)

from api.api_routes import bp

app.blueprint(bp)
