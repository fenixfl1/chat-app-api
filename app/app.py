from flask_socketio import send, emit
from .ext import socketio


@socketio.on('message')
def handle_message(msg: str) -> None:
    print(msg)
    send(msg, broadcast=True)
