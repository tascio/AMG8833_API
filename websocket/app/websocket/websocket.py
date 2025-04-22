from flask_socketio import emit, SocketIO
from websocket import rts
import eventlet


def register_websocket_events(socketio, rts, logger):
    @socketio.on('connect')
    def handle_connect():
        print('ok')
        emit('message', {'status': 'connected'})
        logger.info('[SocketIO] Client connected')

    @socketio.on('disconnect')
    def handle_disconnect():
        logger.info('[SocketIO] Client disconnected')


    def background_emit():
        while True:
            try:
                data = {
                    't_max': rts.get('t_max')[1],
                    't_thermistor': rts.get('t_thermistor')[1],
                }

                # t_array
                keys = [f'array{row}{col}' for row in range(8) for col in range(8)]
                array_data = {key: rts.get(key)[1] for key in keys}
                data['t_array'] = array_data

                socketio.emit('sensor_data', data)
                eventlet.sleep(0.2)  
            except Exception as e:
                logger.error(f"[WebSocket] Error during background emit: {e}")
                eventlet.sleep(1)

    socketio.start_background_task(background_emit)
    logger.info('Start WebSocket')
