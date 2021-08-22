from flask import Flask
from .ext import socketio, login, jwt


def create_app(settings_module: str) -> Flask:
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_object(settings_module)

    socketio.init_app(app, cors_allowed_origins="*")
    login.init_app(app)
    jwt.init_app(app)

    if app.config.get('TESTING', True):
        print(" * Running in development mode")
        app.config.from_envvar('APP_DEVELOPMENT_SETTINGS', silent=True)
    else:
        print(" * Running in production mode")
        app.config.from_envvar('APP_PRODUCTION_SETTINGS', silent=True)

    from .auth import bp_auth
    app.register_blueprint(bp_auth)

    return app
