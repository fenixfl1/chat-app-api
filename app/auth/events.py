from flask_socketio import send
from app.ext import socketio


@socketio.on('connect')
def connect():
    print("connected")


@socketio.on('message')
def handle_message(msg: str) -> None:
    print(msg)
    send(msg, broadcast=True)
