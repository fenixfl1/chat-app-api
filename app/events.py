from flask_socketio import send, emit, join_room
from app.ext import socketio
from flask_jwt_extended import jwt_required
from flask import request, g
from app.utils.constant import *
from app.globals import current_user


@socketio.on('connect')
def connect():
    emit({'username': 'user'}, broadcast=True)


@socketio.on('message')
def handle_message(msg: str) -> None:
    print(msg)
    send(msg, broadcast=True)


@socketio.on(SEND_MESSAGES)
def handle_message(msg: object):
    print(current_user)
    print("_____************************************_____")
    send(msg, broadcast=True)


@socketio.on(SEND_JOIN_REQUEST)
def handle_join_request(data):
    join_room('room1', sid=request.sid)