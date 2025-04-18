from flask import Flask
from redistimeseries.client import Client as RedisTimeSeries
from main.logger import logger
import os

try:
    rts = RedisTimeSeries(host='redis_store_container', port=6379)
except Exception as e:
    logger.critical(f'Redis not initialized {e}')

def create_app():
    BASEDIR = os.path.abspath(os.path.dirname(__file__))
    app = Flask(__name__,)

    # from main.routes import main_blueprint
    # app.register_blueprint(main_blueprint)

    from api.endpoints import api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api/v1.0')


    from api import manager
    manager.main(rts)

    return app