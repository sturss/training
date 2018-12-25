"""
    Module with initializing Sanic application
"""
from sanic import Sanic

from common.zookeeper import ZookeeperManager
from common.redis import RedisManager
from common.kafka import Consumer
from api.config import Configs
from api.api_routes import bp

app = Sanic(__name__)
app.blueprint(bp)


@app.listener("after_server_start")
async def before_start(app, loop):
    if Configs['OFFSET_STORAGE'] == 'ZOOKEEPER':
        await ZookeeperManager.connect()
    else:
        await RedisManager.connect()
    await Consumer.connect()


@app.listener("after_server_stop")
async def after_stop(app, loop):
    if Configs['OFFSET_STORAGE'] == 'ZOOKEEPER':
        await ZookeeperManager.close()
    else:
        await RedisManager.close()
    await Consumer.close()
