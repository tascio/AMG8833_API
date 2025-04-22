from flask_socketio import emit, SocketIO
from flask import request
import eventlet


def main(rts, socketio, logger):

    @socketio.on('connect')
    def handle_connect():
        client_sid = request.sid
        client_ip = request.remote_addr #client_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
        user_agent = request.headers.get('User-Agent', 'unknown')

        emit('message', {'status': 'connected'})
        logger.info(f'[SocketIO] Client connected - SID: {client_sid}, IP: {client_ip}, User-Agent: {user_agent}')

    @socketio.on('disconnect')
    def handle_disconnect():
        client_sid = request.sid
        client_ip = request.remote_addr #client_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
        user_agent = request.headers.get('User-Agent', 'unknown')

        logger.info(f'[SocketIO] Client disconnected - SID: {client_sid}, IP: {client_ip}, User-Agent: {user_agent}')



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
