from flask import Flask, session
from flask_socketio import SocketIO
from .app import socketio
import os


def create_app(settings_module: str or None) -> Flask:
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_object(settings_module)
    app.config['SECRET_KEY'] = os.urandom(24)
    app.config['SESSION_COOKIE_DOMAIN'] = '127.0.0.1'

    socketio.init_app(app, cors_allowed_origins="*")

    @app.after_request
    def after_request(response):
        if '__invalidate__' in session:
            response.delete_cookie(app.session_cookie_name)
        print("__________________________________________")
        print(response)
        print("__________________________________________")
        return response

    return app
