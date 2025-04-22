from websocket import create_app
from websocket import socketio


if __name__ == '__main__':
    app = create_app()
    socketio.run(app, host='0.0.0.0', port=5060)
