from flask import Flask, session
from flask_socketio import SocketIO
from .app import socketio


def create_app(settings_module: str or None) -> Flask:
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_object(settings_module)

    socketio.init_app(app, cors_allowed_origins="*")

    if app.config.get('TESTING', True):
        print(" * Running in development mode")
        app.config.from_envvar('APP_DEVELOPMENT_SETTINGS', silent=True)
    else:
        print(" * Running in production mode")
        app.config.from_envvar('APP_PRODUCTION_SETTINGS', silent=True)

    return app
