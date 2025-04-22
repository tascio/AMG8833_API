from flask import Flask
from flask_socketio import SocketIO
from redistimeseries.client import Client as RedisTimeSeries
from websocket.logger import logger
import os

try:
    logger.info('Redis client initialized')
    rts = RedisTimeSeries(host='redis_store_container', port=6379)
except Exception as e:
    logger.critical(f'Redis not initialized {e}')

def create_app():
    BASEDIR = os.path.abspath(os.path.dirname(__file__))
    app = Flask(__name__)
    socketio = SocketIO(app, logger=True, engineio_logger=True, ping_timeout=20, ping_interval=10) #async_mode='eventlet',

    from websocket.websocket import register_websocket_events
    register_websocket_events(socketio, rts, logger)

    socketio.init_app(app)
    return app, socketio
