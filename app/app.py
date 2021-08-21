from flask_socketio import SocketIO, send, emit


socketio = SocketIO()


@socketio.on('message')
def handle_message(msg: str) -> send:
    print(msg)
    send(msg, broadcast=True)
